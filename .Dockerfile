# 1. Use an official lightweight Python image
FROM python:3.9-slim

# 2. Set the working directory inside the container
WORKDIR /code

# 3. Copy requirements first to leverage Docker cache
COPY requirements.txt .

# 4. Install dependencies
# We use --no-cache-dir to keep the image size small
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of the application code (app folder, frontend folder, .env)
COPY . .

# 6. Command to run the app
# We use ${PORT:-8000} to use Render's dynamic port, or default to 8000 locally
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}