import os
from dotenv import load_dotenv

load_dotenv()

KOLOSAI_API_KEY = os.getenv("KOLOSAI_API_KEY")

if not KOLOSAI_API_KEY:
    raise ValueError("KOLOSAI_API_KEY not found in .env file.")

# Get the absolute path to the directory this file is in
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Go up one level to the root 'shop_assistant' folder
ROOT_DIR = os.path.dirname(BASE_DIR)

# Define storage paths relative to the Root
STORAGE_DIR = os.path.join(ROOT_DIR, "storage")
DB_PATH = os.path.join(STORAGE_DIR, "analytics.db")