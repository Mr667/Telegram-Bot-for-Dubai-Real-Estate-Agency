import logging
import sys
import asyncio
from logging.handlers import RotatingFileHandler

def setup_logger():
    # Create logger
    logger = logging.getLogger("bayut_bot")
    logger.setLevel(logging.INFO)

    # Create formatters
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # System log file handler (rotating)
    system_handler = RotatingFileHandler('system.log', maxBytes=5*1024*1024, backupCount=2)
    system_handler.setFormatter(formatter)
    system_handler.setLevel(logging.INFO)
    logger.addHandler(system_handler)

    # Error log file handler (rotating)
    error_handler = RotatingFileHandler('error.log', maxBytes=5*1024*1024, backupCount=2)
    error_handler.setFormatter(formatter)
    error_handler.setLevel(logging.ERROR)
    logger.addHandler(error_handler)

    return logger

logger = setup_logger()

async def heartbeat():
    """
    Background task to log a heartbeat every 1 hour to ensure the bot is running.
    """
    while True:
        logger.info("HEARTBEAT: The bot is running and healthy.")
        # Sleep for 1 hour
        await asyncio.sleep(3600)
