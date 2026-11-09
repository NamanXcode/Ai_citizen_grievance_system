FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose backend ports
EXPOSE 8000 8001 8002

# Environment variables
ENV PYTHONUNBUFFERED=1 \
    SECRET_KEY=citizen_portal_super_secret_jwt_key_2026 \
    DB_HOST=db \
    DB_PORT=5432 \
    DB_NAME=citizen_portal \
    DB_USER=postgres \
    DB_PASSWORD=Password \
    PORT=8000

# Start unified application, respecting dynamic cloud host PORT if provided
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
