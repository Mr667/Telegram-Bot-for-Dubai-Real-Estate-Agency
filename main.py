import asyncio
import threading
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    ContextTypes
)
from config import Config
from logger import logger, heartbeat
from database import init_db, get_user_session, save_user_session, clear_user_session
from bayut_api import bayut_client
from gsheets_handler import gsheets

# Conversation states
CHOOSING_PURPOSE, CHOOSING_LOCATION, GETTING_PHONE = range(3)

def _get_message_user(update: Update):
    if update.message and update.message.from_user:
        return update.message.from_user
    logger.error("Received update without message or user: %s", update)
    return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user for the property purpose."""
    user = _get_message_user(update)
    if user is None:
        return ConversationHandler.END
    assert update.message is not None
    logger.info(f"User {user.first_name} ({user.id}) started the bot.")
    
    # Initialize session in DB
    await save_user_session(user.id, {"state": "started"})
    
    reply_keyboard = [['For Sale', 'For Rent']]
    await update.message.reply_text(
        "Welcome to the Dubai Real Estate Bot! 🏙️\n\n"
        "Are you looking to buy or rent a property?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True),
    )
    return CHOOSING_PURPOSE

async def purpose_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the chosen purpose and asks for location."""
    user = _get_message_user(update)
    if user is None:
        return ConversationHandler.END
    assert update.message is not None
    text = update.message.text or ""
    purpose = "for-sale" if text == 'For Sale' else "for-rent"
    
    session = await get_user_session(user.id)
    session['purpose'] = purpose
    await save_user_session(user.id, session)

    reply_keyboard = [['Dubai Marina', 'Downtown Dubai', 'JVC', 'Business Bay']]
    await update.message.reply_text(
        f"Great! You are looking for properties {text.lower()}.\n"
        "Which area are you interested in?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    )
    return CHOOSING_LOCATION

async def location_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Fetches properties based on preferences and asks for phone number."""
    user = _get_message_user(update)
    if user is None:
        return ConversationHandler.END
    assert update.message is not None
    location = update.message.text or ""
    
    session = await get_user_session(user.id)
    session['location'] = location
    await save_user_session(user.id, session)

    await update.message.reply_text(
        f"Searching live properties in {location}...",
        reply_markup=ReplyKeyboardRemove()
    )

    # Fetch live data from Bayut API
    properties = await bayut_client.fetch_properties(location=location, purpose=session.get('purpose', 'for-sale'))
    
    if not properties:
        await update.message.reply_text("Sorry, I couldn't find any properties matching your criteria at the moment.")
        return ConversationHandler.END

    # Send property details
    for prop in properties:
        prop_id = prop.get("id", "N/A")
        beds = prop.get("beds", "N/A")
        baths = prop.get("baths", "N/A")
        category = prop.get("category", ["N/A"])
        
        # Get the first 2D image if available
        images_2d = prop.get("2d_imgs", [])
        photo_url = images_2d[0] if images_2d else ""

        msg = f"*Property ID: {prop_id}*\n" \
              f"Beds: {beds} | Baths: {baths}\n" \
              f"Type: {', '.join(category)}"

        if photo_url:
            try:
                await update.message.reply_photo(photo=photo_url, caption=msg, parse_mode="Markdown")
            except Exception as e:
                logger.warning("Failed to send property photo, falling back to text: %s", e)
                await update.message.reply_text(msg, parse_mode="Markdown")
        else:
            await update.message.reply_text(msg, parse_mode="Markdown")

    await update.message.reply_text(
        "If you are interested in any of these, please share your *phone number* (with country code) "
        "and our agent will contact you immediately.",
        parse_mode="Markdown"
    )
    return GETTING_PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Receives phone number, saves lead to Google Sheets, and ends conversation."""
    user = _get_message_user(update)
    if user is None:
        return ConversationHandler.END
    assert update.message is not None
    phone_number = update.message.text or ""
    
    session = await get_user_session(user.id)
    
    search_criteria = f"{session.get('purpose')} in {session.get('location')}"
    
    await update.message.reply_text(
        "Thank you! Your inquiry has been received. "
        "One of our property consultants will call you shortly."
    )

    # Save to Google Sheets asynchronously
    success = await gsheets.add_lead(
        user_id=user.id,
        username=user.username,
        phone_number=phone_number,
        search_criteria=search_criteria,
        selected_property="Not specified"
    )
    
    if success:
        logger.info(f"Lead successfully saved for user {user.id}")
    else:
        logger.error(f"Failed to save lead for user {user.id}")

    # Clear session
    await clear_user_session(user.id)
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = _get_message_user(update)
    if user is None:
        return ConversationHandler.END
    assert update.message is not None
    logger.info("User %s canceled the conversation.", user.first_name)
    await clear_user_session(user.id)
    await update.message.reply_text(
        "Bye! I hope we can help you find a property another time.", 
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

def main() -> None:
    """Run the bot."""
    Config.validate()
    
    # Initialize DB
    asyncio.run(init_db())

    # Create application
    application = Application.builder().token(Config.TELEGRAM_TOKEN).build()

    # Setup conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING_PURPOSE: [MessageHandler(filters.Regex('^(For Sale|For Rent)$'), purpose_choice)],
            CHOOSING_LOCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, location_choice)],
            GETTING_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Start the heartbeat task in a background thread
    heartbeat_thread = threading.Thread(target=lambda: asyncio.run(heartbeat()), daemon=True)
    heartbeat_thread.start()

    # Run the bot
    logger.info("Starting bot polling...")
    application.run_polling()
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user.")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
