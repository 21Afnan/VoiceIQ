FROM python:3.10-slim

# Set working directory
WORKDIR /app

# System dependencies (audio + ML safe)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency config
COPY pyproject.toml .

# Install Python deps
RUN pip install --upgrade pip setuptools wheel \
    && pip install .

# Copy full project
COPY . .

# 🔑 Fix Python imports
ENV PYTHONPATH=/app

# Fly internal port
EXPOSE 8080

# Start FastAPI
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8080"]
