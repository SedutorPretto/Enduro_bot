import os
import sys
import asyncio
import logging

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from aiogram import Bot, Dispatcher
from core.settings import settings
from core.handlers import registration_service, basic, admin_handlers, add_employer
from core.keyboards.set_menu import set_client_menu
from core.database.base import BaseModel


async def start():
    bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')

    dp = Dispatcher()

    await set_client_menu(bot)

    dp.include_router(basic.router)
    dp.include_router(add_employer.router)
    dp.include_router(registration_service.router)
    dp.include_router(admin_handlers.router)
    dp.startup.register(basic.start_bot)
    dp.shutdown.register(basic.stop_bot)

    postgres_url = URL.create(
        'postgresql+asyncpg',
        username=os.getenv('db_user'),
        password=os.getenv('db_password'),
        host=os.getenv('db_host'),
        database=os.getenv('db_name'),
        port=os.getenv('db_port')
    )

    async_engine = create_async_engine(url=postgres_url, echo=True, pool_pre_ping=True)
    session_maker = async_sessionmaker(async_engine, expire_on_commit=False)
    async with async_engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(start())
