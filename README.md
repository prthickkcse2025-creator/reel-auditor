⚡ Speedy AI Auditor
Speedy AI Auditor is a professional-grade AI video analysis tool designed for content creators, social media strategists, and public speakers. It leverages Google’s Gemini 2.5 Flash model to provide an instant, data-driven critique of your video content, focusing on engagement, technical quality, and algorithm performance.

🚀 Features
Comprehensive Audit: Get a detailed breakdown of your video across 12 critical categories, including Hook Strength, Storytelling, and Body Language.

Fast Analysis: Optimized for speed using the latest Gemini Flash models.

Actionable Insights: Receive specific, timestamped feedback on how to improve your content.

Algorithm Focused: Designed specifically to align with Instagram Reel best practices to boost reach and retention.

🛠 Prerequisites
Before running this project, ensure you have the following installed:

Python 3.10+

ffmpeg (Required for efficient video processing/trimming)

A Google AI Studio API Key

Installation
Clone the repository:

Bash
git clone https://github.com/YOUR_USERNAME/speedy-ai-auditor.git
cd speedy-ai-auditor
Create a virtual environment (recommended):

Bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies:

Bash
pip install -r requirements.txt
Configure environment variables:
Create a .env file in the root directory and add your API key:

Plaintext
GOOGLE_API_KEY=your_actual_key_here
🚀 Usage
Run the Streamlit application:

Bash
streamlit run app.py
Open your browser to the URL provided in the terminal (usually http://localhost:8501), upload your .mp4 file, and click "Start Fast Analysis."

💡 How it works
The tool processes your uploaded video through the Gemini API. By utilizing the gemini-2.5-flash model, it performs deep content analysis while maintaining high performance.

Note: For the fastest results, consider trimming your videos to the specific segment you want audited.

🤝 Contributing
Contributions are welcome! If you have suggestions for new features, improved prompts, or bug fixes, feel free to open an issue or submit a pull request.

📄 License
This project is licensed under the MIT License
