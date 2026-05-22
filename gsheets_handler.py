import asyncio
from datetime import datetime
from pathlib import Path

import gspread
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials

from config import Config
from logger import logger

class GSheetsHandler:
    def __init__(self):
        self.scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive"
        ]
        self.creds = None
        self.client = None
        self.sheet = None
        self.setup()

    def setup(self):
        try:
            if not Config.GOOGLE_SHEETS_CREDENTIALS_FILE:
                logger.warning("No Google Sheets credentials file provided.")
                return

            credentials_path = Path(Config.GOOGLE_SHEETS_CREDENTIALS_FILE)
            if not credentials_path.exists():
                logger.error("Google Sheets credentials file not found: %s", credentials_path)
                return

            self.creds = Credentials.from_service_account_file(
                filename=str(credentials_path),
                scopes=self.scope,
            )
            self.client = gspread.authorize(self.creds)

            sheet_identifier = Config.GOOGLE_SHEET_URL_OR_ID
            if not sheet_identifier:
                logger.error("Google Sheets URL or ID is not configured.")
                return

            if "docs.google.com" in sheet_identifier:
                self.sheet = self.client.open_by_url(sheet_identifier).sheet1
            else:
                self.sheet = self.client.open(sheet_identifier).sheet1

            logger.info("Successfully connected to Google Sheets.")
        except Exception as e:
            logger.error(f"Failed to connect to Google Sheets: {e}")

    def _append_lead_sync(self, lead_data: list):
        if not self.sheet:
            logger.error("Cannot append lead: Google Sheets not connected.")
            return False

        try:
            if self.creds and self.creds.expired:
                self.creds.refresh(Request())
                self.client = gspread.authorize(self.creds)

            self.sheet.append_row(lead_data)
            logger.info(f"Successfully appended new lead to Google Sheets: {lead_data[1]}")
            return True
        except Exception as e:
            logger.error(f"Error appending lead to Google Sheets: {e}")
            return False

    async def add_lead(self, user_id, username, phone_number, search_criteria, selected_property):
        """
        Asynchronously adds a lead to Google Sheets to avoid blocking the bot.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lead_data = [
            timestamp,
            str(user_id),
            f"@{username}" if username else "N/A",
            phone_number,
            str(search_criteria),
            str(selected_property)
        ]
        
        # Run the synchronous gspread call in an executor to avoid blocking the async event loop
        loop = asyncio.get_running_loop()
        success = await loop.run_in_executor(None, self._append_lead_sync, lead_data)
        return success

# Global instance
gsheets = GSheetsHandler()
