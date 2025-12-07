import os
from dotenv import load_dotenv

# 1. Define paths first to locate the root
# Get the absolute path to the directory this file is in (app/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Go up one level to the root folder
ROOT_DIR = os.path.dirname(BASE_DIR)

# 2. Load .env explicitly from the ROOT directory
load_dotenv(os.path.join(ROOT_DIR, ".env"))

# 3. Access variables
KOLOSAI_API_KEY = os.getenv("KOLOSAI_API_KEY")

# Admin Credentials (loads from .env, falls back to defaults if missing)
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "Kolosal")

if not KOLOSAI_API_KEY:
    raise ValueError("KOLOSAI_API_KEY not found in .env file.")

# Define storage paths relative to the Root
STORAGE_DIR = os.path.join(ROOT_DIR, "storage")
DB_PATH = os.path.join(STORAGE_DIR, "analytics.db")