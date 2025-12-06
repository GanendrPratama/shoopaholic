# 1. Use Python 3.11 Slim (Lightweight)
FROM python:3.11-slim

# 2. Set working directory
WORKDIR /code

# 3. Install system dependencies (Required for some Python packages)
# We clean up apt lists afterwards to keep the image small
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 4. Upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# 5. Copy requirements
COPY requirements.txt .

# 6. CRITICAL FIX: Install CPU-only PyTorch first
# This prevents downloading the massive 800MB+ GPU version
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# 7. Install the rest of the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 8. Copy application code
COPY . .

# 9. Run the app
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}