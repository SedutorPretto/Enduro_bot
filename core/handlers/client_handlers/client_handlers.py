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


@router.message(Command('contacts'))
async def contacts_view(message: Message):
    await message.answer(text='Позвонить ☎️ +79881421427\n\n'
                              '<a href="http://t.me/enduro23_sochi">Написать в ТГ</a>\n\n'
                              '<a href="http://t.me/enduro23sochi">Наблюдать за нами</a>\n\n'
                              'Проехать:\nСочи, Адлерский район, ул. Краснофлотская, 1а\n\n'
                              '<a href="https://yandex.ru/maps/org/enduro23/125365567287/'
                              '?ll=39.988092%2C43.506737&z=14">Построить маршрут</a>',
                         disable_web_page_preview=True)

@router.message(Command('help'))
async def help_view(message: Message):
    await message.answer()