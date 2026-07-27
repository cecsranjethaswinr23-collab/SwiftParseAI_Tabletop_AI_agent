# 🤖 SwiftParseAI_Tabletop_AI_agent
SwiftParseA is an intelligent, privacy-focused talent evaluation platform built with FastAPI, Streamlit, and Google Gemini. It automates candidate resume screening against job descriptions while enforcing strict local PII (Personally Identifiable Information) masking.

Sensitive contact coordinates—specifically email addresses and phone numbers are stripped locally using Regex before the resume text is transmitted to the LLM. Gemini evaluates skills and match percentages and extracts the candidate's name, while contact informations remains safely isolated within your local environment.

## 📱 Project Application Screenshots

### User Interface

### Output Interface


## 🌟 Key Features
**👾 Local PII Redaction:** Email id and phone numbers are intercepted, extracted, and replaced with [REDACTED] markers locally before external API transmission.

**📁 Instant Backend Storage:** PDF text extraction (pdfplumber) immediately stores preprocessed data upon file upload.

**💯 Semantic Match Scoring:** Powered by Google Gemini for structured evaluation JSON output (Match %, Tech Stack Found, Missing Skills, Evaluation Summary).

**🔗 Decoupled Architecture:** Clean separation between the FastAPI inference engine backend and the Streamlit dashboard UI.


## 🛠️ Tech Stack

**Language:** Python

**Frontend:** Streamlit

**Backend:** FastAPI, Uvicorn

**LLM Engine:** Google Gemini AI

**PDF Extraction & Parsing:** pdfplumber


## 📐 Architecture & Pipeline Flow
```
               [ User PDF Uploads ]
                         │
                         ▼
┌────────────────────────────────────────────────────────┐
│           PDF Text Extraction                          │
│  Converts raw PDFs(JD, Resume) into string text        │
└────────────────────────┬───────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────┐
│        Local PII Redaction & Storage (Regex Engine)    │
│    • Email / Phone ───> Saved Local                    │  (Ensures the safety of personal informations of the candidate
│    • Sanitized Text ──> Prepared for LLM Transmission  │    by not giving it to the LLM)
└────────────────────────┬───────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────┐
│          External AI Processing (Gemini API)           │
│          Input: JD Text + Resume Text                  │
│ Output: Name+ Info + Skills + Match Score + Summary    │
└────────────────────────┬───────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────┐
│         Response Synthesis (FastAPI Layer)             │
│    Combines Gemini JSON output + Local Email/Phone     │
└────────────────────────┬───────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────┐
│        Centered UI Display (Streamlit Frontend)        │
│       Output: candidate match dashboard layout.        │
└────────────────────────────────────────────────────────┘
```

## Project Links & Author

**Repository:** [GitHub](https://github.com/cecsranjethaswinr23-collab/Botanical_Pathology_And_Targeted_Remediation)

**Author:** Ranjeth Aswin Ravindran

**Connect with me:** 👋 [LinkedIn](www.linkedin.com/in/ranjeth-aswin-ravindran-018277253)
                         [GitHub](https://github.com/cecsranjethaswinr23-collab)
