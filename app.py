import os
import re
import json
import pdfplumber
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# webpage name and icon
st.set_page_config(
    page_title="Compliant Prioritizer",
    page_icon="🎫",
    layout="centered"
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
finds the best match for your job description with greater accuracy using LLM(OpenAI)

""")

# sidebar markdown 2
st.sidebar.markdown("""
#### 🫠 WHAT IT IS TRAINED ON:
This model specifically trained on Seven categories of complaint tickets like Banking Services, Credit Card, Consumer Loan, 
Credit Reporting, Debt collection, Mortgage and Student Loan 

""")
st.sidebar.subheader("🛠️ Tech Stack")
tech_stack = [
    "Python",
    "Pandas",
    "Scikit-Learn",
    "Spacy",
    "Transformers",
    "Streamlit",
]
for tech in tech_stack:
    st.sidebar.markdown(f"- **{tech}**")

# github link bar
st.sidebar.subheader("🔗 Source Code")
st.sidebar.link_button("💻 Go to GitHub Repository", "https://github.com/cecsranjethaswinr23-collab/Complaint_Prioritizer_NLP", use_container_width=True)

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