import os
from dotenv import load_dotenv

load_dotenv()

KOLOSAI_API_KEY = os.getenv("KOLOSAI_API_KEY")
PERSIST_DIR = "./storage"  # Where vector data is saved

if not KOLOSAI_API_KEY:
    raise ValueError("KOLOSAI_API_KEY not found in .env file.")