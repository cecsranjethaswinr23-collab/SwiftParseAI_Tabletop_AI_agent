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
This is a executive toy(tabletop toy) for HR(Human Resources) resume screening. 
Swiftly you can screen the resumes by uploading job description and resume. This is an AI Agent who 
finds the best match of resume for your job description with greater accuracy using LLM(OpenAI). Just 
upload a resume and a JD and its done !!!
""")

# sidebar markdown 2
st.sidebar.markdown("""
#### 🫠 PROCEDURE:
The uploading job description and rsume have to be .pdf file.
""")
st.sidebar.subheader("🛠️ Tech Stack")
tech_stack = [
    "Python",
    "Scikit-Learn",
    "Streamlit",
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
st.subheader("Professional single-call pipeline optimized for privacy and latency.")
st.markdown(""" This application recognizes the severity of your problem and categorize it. The complaints with high risk for the consumers
will be recognized by the application and prioritize the tickets for immediate resolving of the problem for better consumer services...
""")

st.write("---")

BACKEND_URL = "[http://127.0.0.1:8000](http://127.0.0.1:8000)"


if "jd_ready" not in st.session_state:
    st.session_state.jd_ready = False
if "resume_ready" not in st.session_state:
    st.session_state.resume_ready = False

c1, c2 = st.columns([1, 1.5], gap="large")

# Left Panel - Job Posting configurations
with c1:
    st.header("Upload Job Description")
    jd_file = st.file_uploader("Choose JD .pdf", type=["pdf"], key="jd_file_picker")
    if jd_file:
        if st.button("💡Configure the JOB PROFILE💡"):
            files = {"file": (jd_file.name, jd_file.getvalue(), "application/pdf")}
            res = requests.post(f"{BACKEND_URL}/upload-jd/", files=files)
            if res.status_code == 200:
                st.session_state.jd_ready = True
                st.success("Job Description locked into Backend Memory!")
            else:
                st.error(f"Error checking JD: {res.text}")

# Right Panel - Candidate screening operations loop
with c2:
    st.header("Upload Resume")
    if st.session_state.jd_ready:
        resume_file = st.file_uploader("Choose Candidate's Resume .pdf", type=["pdf"], key="resume_file_picker")
        
        # AUTOMATIC PREPROCESSING ACTIVATION
        # When a file is dropped into the container slot, this logic triggers right away
        if resume_file:
            # We use a custom flag session attribute to avoid hitting the endpoint on every refresh cycle
            if not st.session_state.resume_ready:
                with st.spinner("Extracting text and removing personal details on backend..."):
                    files = {"file": (resume_file.name, resume_file.getvalue(), "application/pdf")}
                    res = requests.post(f"{BACKEND_URL}/preprocess-resume/", files=files)
                    if res.status_code == 200:
                        st.session_state.resume_ready = True
                    else:
                        st.error(f"Preprocessing failed: {res.text}")
            
            # Show success message once backend signals data masking is finished
            if st.session_state.resume_ready:
                st.success("Resume uploaded and preprocessed successfully!")
                
                # RECRUITER EXPLICIT TRIGGER BUTTON
                if st.button("Run Match Analysis Engine", type="primary"):
                    with st.spinner("Requesting semantic review from Gemini Flash..."):
                        # Fires off to Route 3 which runs the clean anonymized dataset
                        res = requests.post(f"{BACKEND_URL}/evaluate/")
                        
                        if res.status_code == 200:
                            data = res.json()
                            score = data.get("match_percentage", 0)
                            
                            st.write("---")
                            st.metric("Match Score Assessment", f"{score}%")
                            
                            st.markdown("### 📋 Candidate Information")
                            st.text_input("Extracted Full Name (via LLM)", value=data.get("candidate_name"), disabled=True)
                            
                            st.markdown("### 🛠️ Tech Stack Found")
                            st.info(", ".join(data.get("tech_stack_found", [])))
                            
                            st.markdown("### 🔍 Missing Requirements")
                            st.warning(", ".join(data.get("missing_critical_skills", [])) or "None!")
                            
                            st.markdown("### 📝 Analysis Summary")
                            st.write(data.get("summary"))
                        else:
                            st.error(f"Evaluation pipeline error: {res.text}")
                            
        # Reset ready-state conditions if the user cancels out the file completely
        else:
            st.session_state.resume_ready = False
    else:
        st.info("Please set up the Job Description on the left side to get started.")