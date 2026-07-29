FROM python:3.10-slim

ENV PYTHONTONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

# Install system dependencies required for layout parsers and Linux utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy all project modules (app.py, main.py, llm_prompt.py, etc.)
COPY . .

# Convert line endings to Unix LF and grant execution permissions to bootstrapper
RUN sed -i 's/\r$//' start.sh && chmod +x start.sh

# Expose Streamlit and FastAPI ports
EXPOSE 7860
EXPOSE 8000

# Run SwiftParseAI application via process runner
CMD ["./start.sh"]