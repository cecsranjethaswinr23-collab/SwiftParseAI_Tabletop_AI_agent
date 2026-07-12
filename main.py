import os
import re

import json

import pdfplumber

from fastapi import FastAPI, UploadFile, File, HTTPException
from google import genai
from google.genai import types
from dotenv import load_dotenv

from llm_prompt import SYSTEM_PROMPT

# dependancies
#---------------------------------------------------------------------------------------------------------->

load_dotenv() # automatically injects the .env values into your system env

client = genai.Client() # searches your system environment variables

app = FastAPI(title="SwiftParseAI")

contents = {"active_jd_text": None,"masked_resume_text": None} # to hold the data

email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
phnumb_regex = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'

def extract_pdf_text(upload_file: UploadFile) -> str:
    """Validates that a file is a PDF and extracts its text cleanly."""
    if not upload_file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail=f"File '{upload_file.filename}' must be a PDF.")
    
    try:
        text = ""
        with pdfplumber.open(upload_file.file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
                    
        if not text.strip():
            raise HTTPException(status_code=400, detail=f"PDF '{upload_file.filename}' contains no readable text.")
        return text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading PDF layout: {str(e)}")

# --- ROUTE 1: UPLOAD JOB DESCRIPTION ---
@app.post("/upload-jd/")
async def upload_job_description(file: UploadFile = File(...)):
    contents["active_jd_text"] = extract_pdf_text(file)
    return {"status": "success", "message": "Job Description locked into Backend Memory!"}

# --- ROUTE 2: UPLOAD & PREPROCESS RESUME (NO LLM CALL YET) ---
@app.post("/preprocess-resume/")
async def preprocess_resume(file: UploadFile = File(...)):
    # Extract the raw text stream
    raw_resume = extract_pdf_text(file)

    email_match = re.search(email_regex, raw_resume)
    phone_match = re.search(phnumb_regex, raw_resume)
    
    contents["cached_email"] = email_match.group(0) if email_match else "Not Found"
    contents["cached_phone"] = phone_match.group(0) if phone_match else "Not Found"
    # Securely mask the phone number and email instantly before saving to session memory
    # This guarantees that sensitive contact coordinates never leave your machine
    masked_text = re.sub(email_regex, "[EMAIL]", raw_resume)
    masked_text = re.sub(phnumb_regex, "[PHONE]", masked_text)
    
    contents["masked_resume_text"] = masked_text
    return {"status": "success", "message": "Resume uploaded and preprocessed successfully!"}

# --- ROUTE 3: EXECUTE GEMINI EVALUATION ---
@app.post("/evaluate/")
async def evaluate_match():
    if not contents["active_jd_text"]:
        raise HTTPException(status_code=400, detail="Missing active Job Description context.")
    if not contents["masked_resume_text"]:
        raise HTTPException(status_code=400, detail="Missing preprocessed candidate data stream.")
        
    try:
        instance_content = f"JOB DESCRIPTION:\n{contents['active_jd_text']}\n\nRESUME:\n{contents['masked_resume_text']}"
        
        # Call Gemini using the recommended flash model configuration
        response = client.models.generate_content(
            model='gemini-3.5-flash',
            contents=instance_content,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                response_mime_type="application/json", # Forces Gemini to return pure valid JSON
                temperature=0.2
            )
        )
        
        # Load string block directly into standard JSON mapping dictionary
        result_data = json.loads(response.text)

        result_data["email"] = contents["cached_email"]
        result_data["phone"] = contents["cached_phone"]
        
        return result_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Google AI Studio Inference Failed: {str(e)}")