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

# Define the retry logic for the API call
@retry(
    stop=stop_after_attempt(3), 
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(Exception),
    reraise=True
)
def generate_report_with_retry(video_file, prompt):
    # Using gemini-2.0-flash as it is the most stable and fast model
    return client.models.generate_content(
        model="gemini-2.0-flash", 
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

                st.write("Generating report (Retrying if server is busy)...")
                prompt = '''[INSERT YOUR ELITE PROMPT HERE]'''
                
                # Call the retry-protected function
                response = generate_report_with_retry(video_file, prompt)
                
                status.update(label="Analysis Complete!", state="complete")
            
            st.markdown(response.text)
            
        except Exception as e:
            # Check for 503 error specifically for a friendlier message
            if "503" in str(e) or "UNAVAILABLE" in str(e):
                st.error("The AI server is currently at peak capacity. Please try again in a few moments.")
            else:
                st.error(f"Analysis Error: {e}")
            
        finally:
            if video_file:
                try:
                    client.files.delete(name=video_file.name)
                except:
                    pass
            if os.path.exists(temp_path):
                os.remove(temp_path)
