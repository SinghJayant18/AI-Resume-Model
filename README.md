# Smart Resume Tailor — ATS-Friendly Resume Optimizer (Gemini API)

An interactive **Streamlit** application that uses **Google Gemini 1.5 Flash** to analyze and tailor resumes for Applicant Tracking Systems (ATS). 
It identifies matching and missing skills, evaluates your work experience relevance, suggests improvements, and generates a fully tailored, ready-to-download resume that increases your chances of getting shortlisted.

---

## ✨ Features
- **Resume Upload** — Supports PDF, DOCX, and TXT formats.
- **ATS Match Scoring** — Calculates score based on skills & experiences overlap.
- **Matched / Missing Skills** — See what you have vs. what you need.
- **Project Suggestions** — Generates dummy projects with tech stack & measurable improvements.
- **Tailored Resume** — ATS-optimized with Name, Contact, Summary, Skills, Experience, and Education.
- **Download as DOCX** — Save your tailored resume instantly.

---

## 📦 Installation

1. **Clone the repository**
```bash
git clone https://github.com/SinghJayant18/AI-Resume-Model.git
cd AI-Resume-Model
```

2. **Create & activate a virtual environment** (optional but recommended)
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**  
Create a `.env` file in the project root:
```
API_KEY=your_google_gemini_api_key_here
```

---

## 🚀 Usage

Run the Streamlit app:
```bash
streamlit run app.py
```

Steps inside the app:
1. Upload your resume (PDF, DOCX, TXT)
2. Paste the job description
3. Click **"Analyze & Tailor"**
4. Review:
   - ATS Match Score
   - Matched / Missing Skills
   - Tailored Resume
5. Download your optimized resume as a DOCX file.

---

## 🛠 Built With
- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [pdfplumber](https://pypi.org/project/pdfplumber/)
- [python-docx](https://python-docx.readthedocs.io/)
- [google-generativeai](https://ai.google.dev/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

---


