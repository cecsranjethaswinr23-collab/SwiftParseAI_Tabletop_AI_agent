FROM python:3.10-slim

WORKDIR /app

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose Streamlit and FastAPI ports
EXPOSE 7860
EXPOSE 8000

# Run FastAPI in the background and Streamlit in the foreground
CMD uvicorn main:app --host 0.0.0.0 --port 8000 & streamlit run app.py --server.port 7860 --server.address 0.0.0.0