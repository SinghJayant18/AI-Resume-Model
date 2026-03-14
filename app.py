import streamlit as st
import pdfplumber
from docx import Document
import io
import os
from dotenv import load_dotenv
import google.generativeai as genai

# --------------------
# Load Environment Variables
# --------------------
load_dotenv()

# --------------------
# Gemini API Config
# --------------------
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

MODEL_NAME = "gemini-1.5-flash"

# --------------------
# Streamlit Page Setup
# --------------------
st.set_page_config(
    page_title="Smart Resume Tailor (Gemini)",
    layout="wide"
)

st.title("Smart Resume Tailor — ATS Resume Optimizer")
st.write(
    "Upload your resume and paste a job description. "
    "The app will analyze ATS compatibility and generate an optimized resume."
)

st.sidebar.info(f"Using Gemini Model: {MODEL_NAME}")

# --------------------
# File Upload
# --------------------
uploaded_file = st.file_uploader(
    "Upload Resume (PDF / DOCX / TXT)",
    type=["pdf", "docx", "txt"]
)

job_desc = st.text_area(
    "Paste Job Description",
    height=200
)

# --------------------
# Helper: Extract Text
# --------------------
def extract_text_from_file(uploaded_file):
    if uploaded_file is None:
        return ""

    file_name = uploaded_file.name.lower()
    data = uploaded_file.getvalue()

    if file_name.endswith(".pdf"):
        text = ""
        with pdfplumber.open(io.BytesIO(data)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text

    elif file_name.endswith(".docx"):
        doc = Document(io.BytesIO(data))
        return "\n".join([p.text for p in doc.paragraphs if p.text])

    elif file_name.endswith(".txt"):
        return data.decode("utf-8", errors="ignore")

    return ""

# --------------------
# Gemini Prompt Function
# --------------------
def gemini_prompt(system_prompt, user_prompt):
    model = genai.GenerativeModel(MODEL_NAME)

    full_prompt = f"""
{system_prompt}

{user_prompt}
"""

    response = model.generate_content(full_prompt)

    return response.text.strip()


# --------------------
# Main Analysis Button
# --------------------
if st.button("Analyze & Tailor Resume"):

    if not uploaded_file:
        st.error("Please upload your resume.")
        st.stop()

    if not job_desc.strip():
        st.error("Please paste a job description.")
        st.stop()

    with st.spinner("Extracting Resume Text..."):
        resume_text = extract_text_from_file(uploaded_file)

    st.subheader("Extracted Resume")
    st.text_area("Resume Content", resume_text, height=250)

    # --------------------
    # Gemini Prompt
    # --------------------
    unified_prompt = f"""
Given the ORIGINAL RESUME and JOB DESCRIPTION below:

Tasks:

1. Calculate ATS match score (0–100%).
2. Return:
   - ATS match score
   - Matched skills
   - Missing skills

3. Generate:
   - Dummy projects matching the job description
   - Suggested projects with tech stack and improvements
   - 2–3 line professional summary
   - ATS optimized resume

Use this format:

ATS Match Score: X%

Matched Skills: skill1, skill2

Missing Skills: skill1, skill2

Professional Summary:
...

Suggested Projects:
...

Optimized Resume:
(Name, Contact, Summary, Skills, Experience, Education)

Improvement Suggestions:
...

ORIGINAL RESUME:
{resume_text}

JOB DESCRIPTION:
{job_desc}
"""

    with st.spinner("Analyzing Resume with Gemini..."):
        result = gemini_prompt(
            "You are an expert ATS resume analyzer and resume writer.",
            unified_prompt
        )

    # --------------------
    # Parse ATS Score
    # --------------------
    score = 0
    matched = []
    missing = []

    lines = result.split("\n")

    for line in lines:

        lower = line.lower()

        if "match score" in lower:
            digits = "".join(filter(str.isdigit, line))
            if digits:
                score = int(digits)

        if "matched skills" in lower:
            matched = [x.strip() for x in line.split(":")[-1].split(",")]

        if "missing skills" in lower:
            missing = [x.strip() for x in line.split(":")[-1].split(",")]

    # --------------------
    # Show Results
    # --------------------
    st.metric("ATS Match Score", f"{score}%")

    st.subheader("Matched Skills")
    st.write(matched)

    st.subheader("Missing Skills")
    st.write(missing)

    st.subheader("Tailored Resume Output")
    st.write(result)

    # --------------------
    # Generate DOCX Download
    # --------------------
    doc_buffer = io.BytesIO()

    doc = Document()

    for line in result.split("\n"):
        doc.add_paragraph(line)

    doc.save(doc_buffer)

    doc_buffer.seek(0)

    st.download_button(
        label="Download Tailored Resume (DOCX)",
        data=doc_buffer,
        file_name="tailored_resume.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

    st.success("Resume tailored successfully!")


else:
    st.info("Upload a resume and paste a job description to begin.")

# --------------------
# Sidebar Info
# --------------------
st.sidebar.markdown("### About")
st.sidebar.markdown(
    "This tool analyzes your resume and job description to generate an ATS optimized resume using Google Gemini."
)

st.sidebar.markdown("### Privacy")
st.sidebar.markdown(
    "Your resume and job description are processed temporarily and not stored."
)

st.sidebar.markdown("### License")
st.sidebar.markdown(
    "This project is for educational purposes."
)
