import os

from pathlib import Path

from dotenv import load_dotenv


# Load .env file
load_dotenv()


# Project directory
BASE_DIR = Path(__file__).resolve().parent.parent


# =========================
# Application Settings
# =========================

APP_NAME = "PocketSmart AI"


# =========================
# Security Settings
# =========================

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "change-this-secret-key"
)

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv(
        "ACCESS_TOKEN_EXPIRE_MINUTES",
        "60"
    )
)


# =========================
# Database
# =========================

DATABASE_PATH = BASE_DIR / "pocketsmart.db"


# =========================
# Uploads
# =========================

UPLOAD_DIR = BASE_DIR / "uploads"

UPLOAD_DIR.mkdir(
    exist_ok=True
)


MAX_UPLOAD_SIZE = 5 * 1024 * 1024


# =========================
# Gemini AI
# =========================

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY",
    ""
)

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    ""
)