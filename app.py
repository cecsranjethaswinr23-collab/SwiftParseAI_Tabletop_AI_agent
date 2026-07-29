import os
import streamlit as st
import requests

# webpage name and icon
st.set_page_config(
    page_title="SwiftParse_AI",
    page_icon="🤖",
    layout="wide"
)
# ----------------------------------------------------------------------------------------------------------------------

# Sidebar
# About title
st.sidebar.title("About")

# sidebar markdown 1
st.sidebar.markdown("""
### 🎯 WHAT IT DOES:
This is a executive toy(tabletop toy) for HR(Human Resources)to screen resume. 
Swiftly you can screen the resumes by uploading job description and resume. This is an AI Agent who 
finds the best match of resume for your job description with greater accuracy using LLM(Gemini AI). Just 
upload a JD, a resume and hit the button and its done !!!
""")

# sidebar markdown 2
st.sidebar.markdown("""
#### 🫠 PROCEDURE:
The uploading job description and rsume have to be .pdf file.
""")
st.sidebar.subheader("🛠️ Tech Stack")
tech_stack = [
    "Python",
    "Streamlit",
    "FastAPI",
    "Py PDF Plumber",
    "Gemini AI"
]
for tech in tech_stack:
    st.sidebar.markdown(f"- **{tech}**")

# github link bar
st.sidebar.subheader("🔗 Source Code")
st.sidebar.link_button("💻 Go to GitHub Repository", "https://github.com/cecsranjethaswinr23-collab/SwiftParseAI_Tabletop_AI_agent", use_container_width=True)

# author bar
st.sidebar.markdown("### 👨‍💻 Developed By")
st.sidebar.markdown("**Ranjeth Aswin Ravindran**")
st.sidebar.caption("Data Scientist")

# Email bar
st.sidebar.markdown("""
📧 **Contact:** cecsranjethaswinr23@gmail.com
""")
# end of about section
# ------------------------------------------------------------------------------------------------------------------------------------

# Main page 

# 1. title
st.title("SwiftParse AI 🤖")
st.subheader("Professional Resume screening AI application")
st.markdown("""SwiftParse AI is a candidate screening application that leverages FastAPI and Google Gemini 
to evaluate applicant resumes while securely scrubbing sensitive contact details (emails and phone numbers) locally before 
any data leaves your system.

To use it, upload your target Job Description on the left to lock the hiring criteria, drop a candidate resume on the 
right to trigger instant automated preprocessing, and hit it to securely render a centered, comprehensive talent evaluation.
""")

st.write("---")

BACKEND_URL = "http://127.0.0.1:8000"

 # initially given false, then given true after the fastapi response
if "jd_ready" not in st.session_state:
    st.session_state.jd_ready = False
if "resume_ready" not in st.session_state:
    st.session_state.resume_ready = False

c1, c2 = st.columns([1, 1], gap="large")

with c1:
    st.header("Upload Job Description")
    jd_file = st.file_uploader("Choose JD .pdf", type=["pdf"], key="jd_file")
    if jd_file:
        if st.button("Configure the JOB PROFILE💡"):
            files = {"file": (jd_file.name, jd_file.getvalue(), "application/pdf")}
            res = requests.post(f"{BACKEND_URL}/upload-jd/", files=files)
            if res.status_code == 200:
                st.session_state.jd_ready = True
                st.success("Job Description noted ✅️")
            else:
                st.error(f"Error checking JD: {res.text}")


with c2:
    st.header("Upload Resume")
    if st.session_state.jd_ready:
        resume_file = st.file_uploader("Choose Resume .pdf", type=["pdf"], key="resume_file ")
        
        if resume_file:
            if not st.session_state.resume_ready:
                with st.spinner("Acknowledging the Resume"):
                    files = {"file": (resume_file.name, resume_file.getvalue(), "application/pdf")}
                    res = requests.post(f"{BACKEND_URL}/preprocess-resume/", files=files)
                    if res.status_code == 200:
                        st.session_state.resume_ready = True
                    else:
                        st.error(f"Preprocessing failed: {res.text}")
            
            if st.session_state.resume_ready:
                st.success("Resume uploaded and preprocessed successfully!")
                
                
                trigger_analysis = st.button("Run Analysis", type="primary")
        else:
            st.session_state.resume_ready = False
    else:
        st.info("Please set up the Job Description on the left side to get started.")



if st.session_state.jd_ready and st.session_state.resume_ready and 'trigger_analysis' in locals() and trigger_analysis:
    st.write("---")
    
    # We use empty side-columns to perfectly force our results into a wide center card layout
    _, center_layout, _ = st.columns([0.15, 0.7, 0.15])
    
    with center_layout:
        with st.spinner("Requesting semantic review from Gemini..."):
            res = requests.post(f"{BACKEND_URL}/evaluate/")
            
            if res.status_code == 200:
                data = res.json()
                score = data.get("match_percentage", 0)
                
                st.markdown("<h2 style='text-align: center;'>Pipeline Diagnostic Metrics</h2>", unsafe_allow_html=True)
                st.metric("Match Score Assessment", f"{score}%")
                
                st.markdown("### 📋 Candidate Information")
                st.text_input("Candidate's Name", value=data.get("candidate_name"), disabled=True)
                
                # Render the regex extracted contact info alongside the centered results
                
                st.text_input(" ✍🏻 Candidate's Email", value=data.get("email"), disabled=True)
                st.text_input("Candidate's contact Number", value=data.get("phone"), disabled=True)
                
                st.markdown("### 🛠️ Tech Stack Found")
                st.info(", ".join(data.get("tech_stack_found", [])))
                
                st.markdown("### 🔍 Missing Requirements")
                st.warning(", ".join(data.get("missing_critical_skills", [])) or "None!")
                
                st.markdown("### 📝 Analysis Summary")
                st.write(data.get("summary"))
            else:
                st.error(f"Evaluation pipeline error: {res.text}") 