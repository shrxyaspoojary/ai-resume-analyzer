import streamlit as st
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

# ---------------- DARK THEME ----------------
st.markdown("""
<style>

/* -------- APP BACKGROUND -------- */
.stApp {
    background-color: #0f172a;
    background-image: radial-gradient(#1e293b 1px, transparent 1px);
    background-size: 20px 20px;
}

/* -------- TEXT -------- */
h1, h2, h3, h4, h5, h6, p, div {
    color: #e2e8f0;
}

/* -------- FILE UPLOADER (BLUE) -------- */
[data-testid="stFileUploader"] {
    background: linear-gradient(135deg, #1e3a8a, #2563eb);
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #3b82f6;
}

/* -------- TEXT AREA (PURPLE) -------- */
textarea {
    background: linear-gradient(135deg, #4c1d95, #7c3aed) !important;
    color: white !important;
    border-radius: 12px !important;
    border: 1px solid #a78bfa !important;
    padding: 10px !important;
}

/* -------- INPUT TEXT -------- */
textarea::placeholder {
    color: #ddd !important;
}

/* -------- BUTTON STYLE -------- */
button {
    background: linear-gradient(135deg, #22c55e, #16a34a) !important;
    color: white !important;
    border-radius: 8px !important;
}

/* -------- SUCCESS BOX -------- */
.stSuccess {
    background-color: #065f46 !important;
}

/* -------- WARNING BOX -------- */
.stWarning {
    background-color: #78350f !important;
}

/* -------- INFO BOX -------- */
.stInfo {
    background-color: #1e3a8a !important;
}

</style>
""", unsafe_allow_html=True)

# ---------------- NAVBAR ----------------
st.markdown("""
<div style="
    position: sticky;
    top: 0;
    background: rgba(2,6,23,0.95);
    padding: 12px 25px;
    border-radius: 10px;
    margin-bottom: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
">
    <div style="display:flex; align-items:center; gap:10px;">
        <div style="font-size:20px; font-weight:600;">AI Resume Analyzer</div>
    </div>
    <div style="font-size:14px; color:#94a3b8;">
        Smart Resume Matching System
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
col1, col2 = st.columns([1, 14])

with col1:
    st.image("logo.png", width=70)

with col2:
    st.markdown("""
    <h1 style='margin-bottom:0; padding-top:10px;'>
         Resume Analyzer + Job Matcher
    </h1>
    <p style='color:#94a3b8; margin-top:0;'>
        Smart Resume Matching System
    </p>
    """, unsafe_allow_html=True)

# ---------------- SKILLS ----------------
skills_list = [
    "python", "java", "sql", "excel",
    "machine learning", "data analysis",
    "c++", "html", "css", "javascript"
]

# ---------------- FUNCTIONS ----------------
def extract_skills(text):
    text = text.lower()
    return [skill for skill in skills_list if skill in text]


def match_score(resume, job):
    cv = CountVectorizer()
    matrix = cv.fit_transform([resume, job])
    score = cosine_similarity(matrix)[0][1]
    return round(score * 100, 2)


def missing_skills(resume_skills, job_skills):
    return list(set(job_skills) - set(resume_skills))


def generate_suggestions(missing):
    return [f"Learn {skill}" for skill in missing]


def extract_details(text):
    details = {}

    # Email
    email = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}", text)
    details["email"] = email[0] if email else "Not found"

    # Phone
    phone = re.findall(r"\+?\d[\d\s-]{8,}\d", text)
    details["phone"] = phone[0] if phone else "Not found"

    # Name (first line assumption)
    lines = text.strip().split("\n")
    details["name"] = lines[0] if lines else "Not found"

    return details


def format_resume(text):
    sections = {
        "SUMMARY": "",
        "EDUCATION": "",
        "SKILLS": "",
        "PROJECTS": "",
        "COURSES": "",
        "OTHERS": ""
    }

    current = "OTHERS"
    for line in text.split("\n"):
        l = line.upper()

        if "SUMMARY" in l:
            current = "SUMMARY"
        elif "EDUCATION" in l:
            current = "EDUCATION"
        elif "SKILLS" in l:
            current = "SKILLS"
        elif "PROJECT" in l:
            current = "PROJECTS"
        elif "COURSE" in l or "WORKSHOP" in l:
            current = "COURSES"

        sections[current] += line + "\n"

    return sections

# ---------------- INPUT ----------------
col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader(" Upload Resume (PDF)", type=["pdf"])

with col2:
    job_desc = st.text_area(" Paste Job Description")

# ---------------- MAIN LOGIC ----------------
if uploaded_file is not None:
    st.success("File uploaded successfully!")

    reader = PdfReader(uploaded_file)
    text = ""

    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()

    # -------- PERSONAL DETAILS --------
    details = extract_details(text)

    st.subheader("👤 Personal Details")
    st.success(f"👤 Name: {details['name']}")
    st.info(f"📧 Email: {details['email']}")
    st.warning(f"📞 Phone: {details['phone']}")

    # -------- STRUCTURED RESUME --------
    st.subheader(" Structured Resume")
    formatted = format_resume(text)

    for section, content in formatted.items():
        if content.strip():
            st.markdown(f"### {section}")
            st.write(content)
            st.markdown("---")

    # -------- SKILLS --------
    skills = extract_skills(text)

    st.subheader(" Extracted Skills")
    if skills:
        st.success(", ".join(skills))
    else:
        st.warning("No skills detected")

    # -------- MATCHING --------
    if job_desc:
        score = match_score(text, job_desc)

        st.subheader(" Match Score")
        st.progress(score / 100)
        st.success(f"{score}% Match")

        job_skills = extract_skills(job_desc)

        st.subheader(" Job Skills")
        st.write(", ".join(job_skills))

        missing = missing_skills(skills, job_skills)

        st.subheader(" Missing Skills")
        if missing:
            st.warning(", ".join(missing))
        else:
            st.success("No missing skills 🎉")

        suggestions = generate_suggestions(missing)

        st.subheader(" Suggestions")
        for s in suggestions:
            st.info(s)

# ---------------- FOOTER ----------------
st.markdown("""
<hr style="margin-top:50px; border:1px solid #1e293b;">

<div style="text-align:center; padding:10px;">
    <p style="color:#94a3b8; font-size:14px;">
        © 2026 AI Resume Analyzer | Built by Shreyas S
    </p>
</div>
""", unsafe_allow_html=True)