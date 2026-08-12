import os
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession

from config import BOT_TOKEN
from database import init_db
from handlers.start import router as start_router

PROXY_URL = os.getenv("PROXY_URL")

async def main():
    logging.basicConfig(level=logging.INFO)
    
    print("Инициализация базы данных...")
    await init_db()
    
    if PROXY_URL:
        print(f"Запуск через прокси: {PROXY_URL.split('@')[-1]}")
        session = AiohttpSession(proxy=PROXY_URL)
        bot = Bot(token=BOT_TOKEN, session=session)
    else:
        print("Запуск без прокси...")
        bot = Bot(token=BOT_TOKEN)
        
    dp = Dispatcher()
    dp.include_router(start_router)
    
    print("Бот успешно запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
