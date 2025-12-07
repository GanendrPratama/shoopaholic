import os
from dotenv import load_dotenv

# 1. Determine Directory Paths
# Get the absolute path to the directory this file is in (e.g., /project/app)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Go up one level to the root folder (e.g., /project)
ROOT_DIR = os.path.dirname(BASE_DIR)

# 2. Load .env from the ROOT directory
# This ensures we grab the file from the project root, not inside /app
dotenv_path = os.path.join(ROOT_DIR, ".env")

# Load the specific env file
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    # Optional: Print warning if file is missing (useful for debugging Docker/Cloud)
    # This is NOT an error in production (Railway injects vars directly)
    print(f"⚠️ Notice: .env file not found at {dotenv_path}. Relying on system environment variables.")

# 3. Retrieve Variables
KOLOSAI_API_KEY = os.getenv("KOLOSAI_API_KEY")

if not KOLOSAI_API_KEY:
    # Raise a helpful error if the key is missing
    # This might cause a startup crash if you forget to set the var in Railway
    raise ValueError(f"KOLOSAI_API_KEY not found. Please ensure it is set in {dotenv_path} or system environment variables.")

# Define storage paths relative to the Root
STORAGE_DIR = os.path.join(ROOT_DIR, "storage")
DB_PATH = os.path.join(STORAGE_DIR, "analytics.db")