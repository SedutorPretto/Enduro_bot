from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from core.database.models import Staff

router = Router()


@router.message(Command('instructors'))
async def instructors_view(message: Message, session_maker: sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(select(Staff).filter(Staff.position == 'инструктор'))
            instructors = result.scalars()
    for ins in instructors:
        await message.answer_photo(ins.telegram_photo,
                                   caption=f'{ins.first_name} {ins.surname}')
