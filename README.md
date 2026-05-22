# Dubai Real Estate Telegram Bot 🏙️

A 24/7 production-ready Telegram Bot built with Python and `python-telegram-bot` to help users find real estate listings in Dubai. It features a conversational interface, fetches live property data (mock Bayut integration provided), captures leads seamlessly into Google Sheets, and uses SQLite for persistent session management.

## Features

- **Conversational Interface**: Interactive menus to choose between Rent/Sale and Location.
- **Live Data Integration**: Fetches property listings asynchronously via a Bayut API client.
- **Lead Capture to Google Sheets**: Connects securely to Google Sheets to automatically save leads (timestamp, username, phone, and criteria) using `gspread`.
- **Session Management**: Lightweight and robust state management using `aiosqlite`.
- **Uptime Monitoring**: A background "Heartbeat" task logs to `system.log` to prove the bot is running 24/7.
- **Production Ready**: Includes both a `Dockerfile` and PM2 `process.json` for easy cloud deployment.

---

## Step-by-Step Setup Guide

### 1. Prerequisites

Before starting, make sure you have:
- **Python 3.10+** (if running locally without Docker)
- A **Telegram Bot Token** from [@BotFather](https://t.me/BotFather)
- A **Google Cloud Project** with the Google Sheets API and Google Drive API enabled.
- A **Google Sheets Credentials JSON file** (Service Account).

### 2. Google Sheets Setup

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Enable the **Google Sheets API** and **Google Drive API**.
3. Create a **Service Account** and generate a JSON key. Save this file as `service_account.json` in the root folder of this project.
4. Create a new Google Sheet. Let's call it "Bayut Bot Leads".
5. **CRITICAL STEP**: Open your `service_account.json` file, find the `client_email` address, and share your new Google Sheet with this email address (give it Editor access).
6. Copy the URL of your Google Sheet.

### 3. Environment Variables

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
2. Open the `.env` file and fill in your details:
   - `TELEGRAM_TOKEN`: Your token from @BotFather.
   - `GOOGLE_SHEETS_CREDENTIALS_FILE`: The name of your json file (e.g., `service_account.json`).
   - `GOOGLE_SHEET_URL_OR_ID`: The full URL of the Google Sheet you created.
   - `BAYUT_API_KEY`: If you have a RapidAPI key for Bayut, enter it here (optional).

### 4. Running Locally (Development)

To run the bot on your own computer:

1. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the bot:
   ```bash
   python main.py
   ```

### 5. Deployment (Production)

To deploy the bot to a Linux server (like AWS, DigitalOcean, or Linode) so it runs 24/7, the easiest way is using Docker.

1. SSH into your server.
2. Clone or copy your bot files to the server.
3. Make sure your `.env` and `service_account.json` are present on the server.
4. Make the deployment script executable and run it:
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```
*This script will automatically install Docker if it's missing, build the bot image, and run it continuously in the background.*

To check the logs on your server:
```bash
docker logs -f bayut-bot_container
```

**Alternative: PM2 Deployment**
If you prefer Node's PM2 instead of Docker:
1. Install PM2: `npm install pm2 -g`
2. Run: `pm2 start process.json`

---

## File Structure

- `main.py`: Core bot logic and Conversation Handlers.
- `bayut_api.py`: Async integration for fetching property data.
- `gsheets_handler.py`: Async integration for appending leads to Google Sheets.
- `database.py`: Async SQLite initialization and session tracking.
- `config.py`: Environment variable management and validation.
- `logger.py`: Rotating file logging and heartbeat task.
- `deploy.sh` & `Dockerfile` & `process.json`: Deployment configurations.
