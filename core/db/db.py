import aiosqlite

DATABASE_FILE = "core/db/database.db"

async def init_db():
    async with aiosqlite.connect(DATABASE_FILE) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER NOT NULL UNIQUE
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER NOT NULL UNIQUE,
                order_text TEXT NOT NULL
            )
        ''')
        await db.commit()


async def add_user(telegram_id):
    async with aiosqlite.connect(DATABASE_FILE) as db:
        await db.execute("INSERT OR IGNORE INTO users (telegram_id) VALUES (?)", (telegram_id,))
        await db.commit()


async def add_application(telegram_id, order_text):
    async with aiosqlite.connect(DATABASE_FILE) as db:
        await db.execute("INSERT OR IGNORE INTO applications (telegram_id, order_text) VALUES (?, ?)", (telegram_id, order_text))
        await db.commit()