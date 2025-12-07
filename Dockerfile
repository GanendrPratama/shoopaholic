# 1. Use Python 3.11 Slim
FROM python:3.11-slim

WORKDIR /code

# 2. Install System Dependencies (ffmpeg, tesseract)
# Added 'curl' to download uv if needed, though we copy it below
RUN apt-get update && apt-get install -y \
    build-essential \
    ffmpeg \
    tesseract-ocr \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# 3. Install 'uv' (The secret weapon for speed)
# This grabs the binary directly, no pip install needed
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# 4. Copy requirements
COPY requirements.txt .

# 5. Install Dependencies using uv (Much faster than pip)
# --system installs into the main python environment
# --index-url forces the CPU version of torch
RUN uv pip install --system --no-cache torch --index-url https://download.pytorch.org/whl/cpu

# 6. Install the rest
RUN uv pip install --system --no-cache -r requirements.txt

# 7. Copy Code
COPY . .

# 8. Run
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}