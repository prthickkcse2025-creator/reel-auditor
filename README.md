# ⚡ Speedy AI Auditor

**Speedy AI Auditor** is a professional-grade AI video analysis tool designed for content creators, social media strategists, and public speakers. It leverages Google’s **Gemini 2.5 Flash** model to provide an instant, data-driven critique of your video content, focusing on engagement, technical quality, and algorithm performance.

---

## 🚀 Features

* **Comprehensive Audit:** Get a detailed breakdown of your video across 12 critical categories, including Hook Strength, Storytelling, and Body Language.
* **Fast Analysis:** Optimized for speed using the latest Gemini Flash models.
* **Actionable Insights:** Receive specific, timestamped feedback on how to improve your content.
* **Algorithm Focused:** Designed specifically to align with Instagram Reel best practices to boost reach and retention.

---

## 🛠 Prerequisites

Before running this project, ensure you have the following installed:

* **Python 3.10+**
* **ffmpeg** (Required for efficient video processing/trimming)
* A **[Google AI Studio API Key](https://aistudio.google.com/)**

---

## ⚙️ Installation

### 1. Clone the repository:
```bash
git clone [https://github.com/YOUR_USERNAME/speedy-ai-auditor.git](https://github.com/YOUR_USERNAME/speedy-ai-auditor.git)
cd speedy-ai-auditor

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

**Create a virtual environment**
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

**Install dependencies:**
pip install -r requirements.txt

**Configure environment variables:**
GOOGLE_API_KEY=your_actual_key_here

## 🚀 Usage
streamlit run app.py

💡 How it works
The tool processes your uploaded video through the Gemini API. By utilizing the gemini-2.5-flash model, it performs deep content analysis while maintaining high performance.

Note: For the fastest results, consider trimming your videos to the specific segment you want audited.

🤝 Contributing
Contributions are welcome! If you have suggestions for new features, improved prompts, or bug fixes, feel free to open an issue or submit a pull request.

## 📄 License

1.  **Missing Newlines:** In Markdown, you must have a blank line before a list (e.g., before the `* Features` list) or it won't render as a bulleted list.
2.  **Missing Backticks:** To get the "code box" look (like for `app.py` or `http://localhost:8501`), you must wrap the text in backticks (the key above your Tab key: `` ` ``).
3.  **Check your Editor:** Make sure you are saving the file as **`README.md`**. If you save it as `README.txt`, it will never show the bold formatting.
