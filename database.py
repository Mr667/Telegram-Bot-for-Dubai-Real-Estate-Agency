import aiosqlite
import json
from logger import logger

DB_FILE = "bot_database.db"

async def init_db():
    """Initialize the database and create tables if they don't exist."""
    try:
        async with aiosqlite.connect(DB_FILE) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS user_sessions (
                    user_id INTEGER PRIMARY KEY,
                    session_data TEXT,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            await db.commit()
            logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")

async def get_user_session(user_id: int) -> dict:
    """Retrieve user session data from the database."""
    try:
        async with aiosqlite.connect(DB_FILE) as db:
            async with db.execute('SELECT session_data FROM user_sessions WHERE user_id = ?', (user_id,)) as cursor:
                row = await cursor.fetchone()
                if row:
                    return json.loads(row[0])
                return {}
    except Exception as e:
        logger.error(f"Error getting user session for {user_id}: {e}")
        return {}

async def save_user_session(user_id: int, session_data: dict):
    """Save or update user session data in the database."""
    try:
        async with aiosqlite.connect(DB_FILE) as db:
            data_str = json.dumps(session_data)
            await db.execute('''
                INSERT INTO user_sessions (user_id, session_data, last_updated)
                VALUES (?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(user_id) DO UPDATE SET
                    session_data = excluded.session_data,
                    last_updated = CURRENT_TIMESTAMP
            ''', (user_id, data_str))
            await db.commit()
    except Exception as e:
        logger.error(f"Error saving user session for {user_id}: {e}")

async def clear_user_session(user_id: int):
    """Clear user session data from the database."""
    try:
        async with aiosqlite.connect(DB_FILE) as db:
            await db.execute('DELETE FROM user_sessions WHERE user_id = ?', (user_id,))
            await db.commit()
    except Exception as e:
        logger.error(f"Error clearing user session for {user_id}: {e}")
