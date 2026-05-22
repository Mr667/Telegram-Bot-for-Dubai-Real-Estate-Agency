# 🏙️ Dubai Real Estate Telegram Bot

![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)
![Telegram Bot API](https://img.shields.io/badge/Telegram%20Bot%20API-python--telegram--bot-2CA5E0.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-Active-success.svg)

A clean, minimalist, and highly efficient Telegram bot built with Python, designed specifically for Dubai real estate agencies. This bot automates property inquiries, showcases premium listings, and acts as a 24/7 lead generation assistant for brokers and agents.

---

## 🤖 What the Bot Does

This bot acts as a digital real estate agent, bridging the gap between property seekers and your agency. It solves the friction of traditional browsing by delivering instant information directly within Telegram.

### For Clients & Investors:
* **Interactive Property Catalog:** Browse through off-plan projects, secondary market properties, or premium rentals in Dubai.
* **Tailored Filtering:** Filter listings by type (Apartment, Villa, Townhouse), price range, and location (e.g., Downtown Dubai, Dubai Marina, JVC).
* **Instant Brochures:** Download floor plans, project brochures, and view high-resolution property galleries instantly.
* **Direct Agent Callback:** Request a callback or WhatsApp connection with a live agent for a specific property with a single click.

### For the Real Estate Agency:
* **24/7 Automated Lead Capture:** Collects user names, phone numbers, and investment preferences even outside regular business hours.
* **Instant Agent Notifications:** Instantly routes qualified buyer leads directly to an internal agency Telegram group or CRM system.
* **Dynamic Catalog Updates:** Agents can add, modify, or archive listings on-the-go via hidden, secure admin commands.

---
Installation
Clone the repository:
git clone [https://github.com/yourusername/dubai-real-estate-bot.git](https://github.com/yourusername/dubai-real-estate-bot.git)
    cd dubai-real-estate-bot
    ```

2.  **Create a virtual environment:**
    
```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    
```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables:**
    Create a `.env` file in the root directory and add your credentials:
    
```env
    BOT_TOKEN=your_telegram_bot_token_here
    ADMIN_ID=your_telegram_user_id
    DATABASE_URL=sqlite:///real_estate.db
    ```

5.  **Initialize the Database & Run:**
    
```bash
    python init_db.py
    python main.py
    ```

---

## 📁 Project Structure

```text
dubai-real-estate-bot/
│
├── main.py                # Entry point of the bot
├── config.py              # Configuration and environment variables
├── requirements.txt       # Python dependencies
├── .env.example           # Example environment variables file
│
├── handlers/              # Command and message handlers
│   ├── start.py           # /start command handler
│   ├── search.py          # Property search flow
│   └── admin.py           # Admin commands for agents
│
├── database/              # Database models and queries
│   ├── models.py          # Database models (Property, User, Lead)
│   └── db_manager.py      # CRUD operations
│
└── assets/                # Default images and localized text
    └── text_responses.json


## ⚙️ How It Works

The bot relies on a conversational state machine architecture to provide a seamless user journey without overwhelming the client.

1 - The Entry & Localization: The user interacts with the bot via /start. The bot identifies the user or prompts them to select a preferred language (e.g., English, Arabic, Russian).

2 - Stateful Conversation Flow: Built using the ConversationHandler from python-telegram-bot. The bot remembers user selections sequentially (Purpose -> Property Type -> Area -> Budget) without storing heavy state data.

3 - Database Matching: Once the filters are set, the bot queries an optimized SQLite/PostgreSQL database to pull active matches, rendering them as "Property Cards" featuring inline buttons for pagination.

4 - The Lead Funnel: When a user clicks "Contact Agent about this Property", the bot initiates a secure contact-sharing workflow. Upon verification, the script packages the user's details along with the specific property ID and triggers a webhook or notification to the agency's broker desk.

```text
 [ User Starts Bot ] ──> [ Selects Language ] ──> [ Main Menu: Buy / Rent / Contact ]
                                                            │
  ┌─────────────────────────────────────────────────────────┘
  ▼
 [ Interactive Filters ] ──> [ Matches Found? ] ──> YES ──> [ Display Property Cards ] ──> [ Click "Interested" ] ──> [ Capture Lead & Notify CRM ]
                                   │
                                   └──> NO ──> [ Offer Custom Consultation Request ]

