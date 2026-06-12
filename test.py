import streamlit as st
import time
import os
from google import genai
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Speedy AI Auditor", layout="wide")
st.title("⚡ AI Video Critique (Fast Mode)")

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("API Key not found. Please set GOOGLE_API_KEY in your .env file.")
    st.stop()

client = genai.Client(api_key=api_key)

# Dynamic model selection function
def get_best_model():
    """Dynamically finds a supported 3.x Flash model."""
    try:
        models = client.models.list()
        # Look for the newest 3.5 flash, fallback to 3.1
        for m in models:
            if "gemini-3.5-flash" in m.name:
                return m.name
            if "gemini-3.1-flash" in m.name:
                return m.name
        return "gemini-3.5-flash" # Default fallback
    except:
        return "gemini-3.5-flash"

# Define the retry logic
@retry(
    stop=stop_after_attempt(3), 
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(Exception),
    reraise=True
)
def generate_report_with_retry(video_file, prompt):
    model_name = get_best_model()
    return client.models.generate_content(
        model=model_name, 
        contents=[video_file, prompt]
    )

uploaded_file = st.file_uploader("Upload video", type=["mp4"])

if uploaded_file:
    temp_path = f"temp_{int(time.time())}_{uploaded_file.name}"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    if st.button("Start Fast Analysis"):
        video_file = None
        try:
            with st.status("Analyzing...", expanded=True) as status:
                st.write("Uploading video...")
                video_file = client.files.upload(file=temp_path)
                
                while video_file.state.name == "PROCESSING":
                    st.write("Processing video on server...")
                    time.sleep(5)
                    video_file = client.files.get(name=video_file.name)
                
                if video_file.state.name == "FAILED":
                    raise Exception("Video processing failed on the server.")

                st.write("Generating report...")
                # Note: Insert your full prompt here
                prompt = "Perform a detailed professional audit of the uploaded video..."
                
                response = generate_report_with_retry(video_file, prompt)
                
                status.update(label="Analysis Complete!", state="complete")
            
            st.markdown(response.text)
            
        except Exception as e:
            error_str = str(e)
            if "503" in error_str or "UNAVAILABLE" in error_str:
                st.error("The AI server is currently at peak capacity. Please try again in a few moments.")
            elif "404" in error_str:
                st.error("The requested model is unavailable. Please check your API access.")
            else:
                st.error(f"Analysis Error: {error_str}")
            
        finally:
            if video_file:
                try: client.files.delete(name=video_file.name)
                except: pass
            if os.path.exists(temp_path):
                os.remove(temp_path)
