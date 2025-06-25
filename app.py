import streamlit as st
from res_parser import extract_text_from_pdf
import os 

def get_available_job_roles():
    role_files = os.listdir("job_roles")
    return [file.replace(".txt", "") for file in role_files if file.endswith(".txt")]


def load_job_keywords(role):
    try:
        with open(f"job_roles/{role}.txt", "r") as f:
            return [line.strip().lower() for line in f.readlines()]
    except FileNotFoundError:
        return []

def match_skills(resume_text, keywords):
    matched = [kw for kw in keywords if kw in resume_text.lower()]
    missing = [kw for kw in keywords if kw not in resume_text.lower()]
    score = round((len(matched) / len(keywords)) * 100, 2) if keywords else 0
    return matched, missing, score


st.set_page_config(page_title="AI Resume Analyzer", layout="centered")

st.title("📄 AI Resume Analyzer")

uploaded_file = st.file_uploader("Upload your resume (PDF only)", type="pdf")

job_roles = get_available_job_roles()
selected_role = st.selectbox("Select a job role", job_roles)

if uploaded_file and selected_role:
    resume_text = extract_text_from_pdf(uploaded_file)

    st.subheader("Extracted Resume Text")
    st.text_area("Resume Content", resume_text, height=600)

    # Load skills and match
    keywords = load_job_keywords(selected_role)
    matched, missing, score = match_skills(resume_text, keywords)

    st.markdown("---")
    st.subheader("✅ Match Results")
    st.write(f"**Match Score:** {score}%")

    st.success(f"**Matched Skills:** {', '.join(matched) if matched else 'None'}")
    st.error(f"**Missing Skills:** {', '.join(missing) if missing else 'None'}")
