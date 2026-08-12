import aiosqlite

DB_NAME = "bot.db"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                telegram_id INTEGER PRIMARY KEY,
                player_tag TEXT NOT NULL
            )
        """)
        await db.commit()

async def add_user(telegram_id: int, player_tag: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            INSERT OR REPLACE INTO users (telegram_id, player_tag)
            VALUES (?, ?)
        """, (telegram_id, player_tag))
        await db.commit()

async def get_player_tag(telegram_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("""
            SELECT player_tag FROM users WHERE telegram_id = ?
        """, (telegram_id,)) as cursor:
            row = await cursor.fetchone()
            if row:
                return row[0]
            return None
