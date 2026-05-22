import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

class Config:
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
    GOOGLE_SHEETS_CREDENTIALS_FILE = os.getenv("GOOGLE_SHEETS_CREDENTIALS_FILE", "service_account.json")
    GOOGLE_SHEET_URL_OR_ID = os.getenv("GOOGLE_SHEET_URL_OR_ID", "")
    BAYUT_API_KEY = os.getenv("BAYUT_API_KEY", "")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

    @classmethod
    def validate(cls):
        missing = []
        if not cls.TELEGRAM_TOKEN:
            missing.append("TELEGRAM_TOKEN")
        if not cls.GOOGLE_SHEETS_CREDENTIALS_FILE:
            missing.append("GOOGLE_SHEETS_CREDENTIALS_FILE")
        if not cls.GOOGLE_SHEET_URL_OR_ID:
            missing.append("GOOGLE_SHEET_URL_OR_ID")
            
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
