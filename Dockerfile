# Backend Dockerfile for Railway deployment
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy and install production requirements (layer cached)
COPY requirements.prod.txt .
RUN pip install --no-cache-dir -r requirements.prod.txt

# Copy application code
COPY src/ ./src/
COPY data/processed/ ./data/processed/
COPY config.yaml .
COPY prompts/ ./prompts/
COPY api_server.py .

# Railway injects PORT env var; default to 8000
ENV PORT=8000

EXPOSE ${PORT}

# Start the FastAPI server (Railway sets $PORT dynamically)
CMD uvicorn api_server:app --host 0.0.0.0 --port ${PORT}
