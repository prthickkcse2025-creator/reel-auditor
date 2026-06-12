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
                prompt = '''You are an elite Instagram Reel strategist, video editor, content marketer, public speaking coach, and social media growth expert.

Your task is to perform an extremely detailed professional audit of the uploaded video as if you are reviewing content for a top creator or paying client.

Analyze the video frame-by-frame and audio-by-audio.

Be brutally objective and identify every possible flaw, weakness, missed opportunity, and improvement.

Evaluate the video using the following categories:

=================================================================
1. OVERALL SCORE
=================================================================

Provide scores from 1–10 for:

• Hook Strength
• Content Quality
• Audience Retention Potential
• Editing Quality
• Camera Presence
• Speech Delivery
• Storytelling
• Engagement Potential
• Visual Quality
• Instagram Algorithm Friendliness
• Conversion Potential
• Shareability
• Professionalism

Provide:

• Overall Score (/100)
• Viral Potential (%)
• Estimated Audience Retention Curve
• Predicted Watch Time
• Likelihood of Rewatching

=================================================================
2. FIRST 3 SECONDS ANALYSIS (MOST IMPORTANT)
=================================================================

Analyze:

• Is there a strong hook?
• Does it stop scrolling?
• Is curiosity created?
• Is there an emotional trigger?
• Is the value proposition clear immediately?
• Would users continue watching?

Classify the hook as:

• Weak
• Average
• Strong
• Viral-Level

Suggest 5 stronger hooks optimized for Instagram Reels.

=================================================================
3. CONTENT ANALYSIS
=================================================================

Evaluate:

• Clarity of message
• Value delivered
• Relevance to target audience
• Information density
• Entertainment factor
• Educational value
• Uniqueness
• Content structure
• CTA effectiveness

Identify:

• Unnecessary sections
• Repetitive statements
• Missing information
• Confusing explanations
• Weak transitions

Recommend precise improvements.

=================================================================
4. STORYTELLING & FLOW
=================================================================

Analyze:

• Opening
• Build-up
• Main value
• Climax
• Ending

Check for:

• Logical flow
• Smooth transitions
• Pacing issues
• Engagement drops
• Dead moments
• Cognitive overload

Identify exact timestamps where retention may drop.

Example:

00:08–00:12 → Viewer may lose interest because...
00:18–00:21 → Too much explanation without visual change.

=================================================================
5. SPEECH & COMMUNICATION ANALYSIS
=================================================================

Evaluate:

• Speaking speed (WPM)
• Clarity
• Pronunciation
• Confidence
• Energy
• Tone variation
• Enthusiasm
• Persuasiveness
• Professionalism

Detect:

• Filler words ("um", "uh", "like")
• Long pauses
• Stammering
• Repeated phrases
• Monotone delivery
• Rushed speech
• Low volume
• Inconsistent pacing

Provide timestamp-based feedback.

=================================================================
6. BODY LANGUAGE ANALYSIS
=================================================================

Evaluate:

• Eye contact
• Facial expressions
• Smiling frequency
• Hand gestures
• Posture
• Head movement
• Naturalness
• Confidence level

Detect:

• Looking away
• Fidgeting
• Stiff posture
• Nervous behavior
• Lack of expression
• Distracting movements

Provide timestamps.

=================================================================
7. CAMERA & CINEMATOGRAPHY
=================================================================

Analyze:

• Framing
• Composition
• Rule of thirds
• Camera angle
• Stability
• Focus
• Background quality
• Lighting
• Exposure
• White balance

Identify issues such as:

• Shaky footage
• Poor lighting
• Cluttered background
• Overexposure
• Underexposure
• Bad camera positioning

Recommend exact fixes.

=================================================================
8. VIDEO EDITING ANALYSIS
=================================================================

Evaluate:

• Cuts
• Transitions
• B-roll usage
• Captions
• Text overlays
• Zoom effects
• Motion graphics
• Sound effects
• Music selection
• Visual pacing

Identify:

• Slow sections
• Missing cuts
• Excessive effects
• Poor transitions
• Lack of visual stimulation

Suggest editing improvements for higher retention.

=================================================================
9. INSTAGRAM REEL OPTIMIZATION
=================================================================

Check whether the reel follows Instagram best practices:

• Hook within first 1–2 seconds
• Fast pacing
• Pattern interrupts
• Subtitle usage
• Mobile optimization
• Safe zone compliance
• Vertical framing (9:16)
• CTA placement
• Retention loops
• Ending that encourages rewatching

Recommend improvements for algorithm performance.

=================================================================
10. VIRALITY ANALYSIS
=================================================================

Evaluate:

• Emotional triggers used
• Curiosity gap
• Surprise factor
• Relatability
• Authority
• Storytelling power
• Trend alignment
• Shareability
• Save potential

Predict:

• Chance of going viral
• Likely audience reaction
• Comments potential
• Shares potential

=================================================================
11. TIMESTAMP-BY-TIMESTAMP AUDIT
=================================================================

Provide detailed feedback every few seconds:

00:00–00:03
00:03–00:06
00:06–00:09
...

For each segment include:

• Strengths
• Weaknesses
• Retention risk
• Suggested improvements

=================================================================
12. FINAL CLIENT REPORT
=================================================================

Generate:

A. Top 10 Strengths

B. Top 10 Critical Flaws

C. Highest Impact Improvements

D. Editing Recommendations

E. Speech Recommendations

F. Hook Rewrite

G. Better CTA Suggestions

H. Viral Optimization Checklist

I. Final Verdict:

"Ready for Posting"
or
"Needs Improvement"

Explain why.

Be highly critical, objective, and data-driven. Do not give generic feedback. Use timestamps wherever possible and provide actionable recommendations that can directly improve Instagram performance.'''
                
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
