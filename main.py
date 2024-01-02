import os
import sys
import asyncio
import logging

from sqlalchemy import URL
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from core.settings import settings
from core.handlers import registration_service, basic, admin_handlers
from core.keyboards.set_menu import set_client_menu
from core.database.engine import crt_async_engine, get_session_maker, proceed_schemas
from core.database.base import BaseModel


async def start():
    bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')

    dp = Dispatcher()

    await set_client_menu(bot)

    dp.include_router(registration_service.router)
    dp.include_router(admin_handlers.router)
    dp.include_router(basic.router)
    dp.startup.register(basic.start_bot)
    dp.shutdown.register(basic.stop_bot)

    postgres_url = URL.create(
        'postgresql+asyncpg',
        username=os.getenv('db_user'),
        host=os.getenv('db_host'),
        database=os.getenv('db_name'),
        port=os.getenv('db_port')
    )

    async_engine = crt_async_engine(postgres_url)
    session_maker = get_session_maker(async_engine)
    await proceed_schemas(async_engine, BaseModel.metadata)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(start())
