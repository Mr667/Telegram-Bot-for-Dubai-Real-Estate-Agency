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

## ⚙️ How It Works

The bot relies on a conversational state machine architecture to provide a seamless user journey without overwhelming the client.

```text
 [ User Starts Bot ] ──> [ Selects Language ] ──> [ Main Menu: Buy / Rent / Contact ]
                                                            │
  ┌─────────────────────────────────────────────────────────┘
  ▼
 [ Interactive Filters ] ──> [ Matches Found? ] ──> YES ──> [ Display Property Cards ] ──> [ Click "Interested" ] ──> [ Capture Lead & Notify CRM ]
                                   │
                                   └──> NO ──> [ Offer Custom Consultation Request ]
