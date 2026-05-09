import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

# Model settings
MODEL_NAME = os.getenv("MODEL_NAME", "llama3.2:3b")

# Gmail settings
GMAIL_CREDENTIALS_PATH = PROJECT_ROOT / "credentials.json"
GMAIL_TOKEN_PATH = PROJECT_ROOT / "token.json"
GMAIL_SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",  # Read + label, NOT delete
    "https://www.googleapis.com/auth/gmail.labels",
]

# Database
DB_PATH = DATA_DIR / "email_agent.db"