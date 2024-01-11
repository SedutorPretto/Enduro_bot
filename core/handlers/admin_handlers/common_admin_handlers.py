from datetime import date, timedelta
from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy import select, extract
from sqlalchemy.orm import sessionmaker

from core.utils.admin import dict_from_message
from core.handlers.states import ConfirmRegistration
from core.database.models import Staff

router = Router()


@router.message(Command('confirm_record'))
async def confirm_record(message: Message,  state: FSMContext):
    await message.answer(text='Выбери запись которую нужно подтвердить')
    await state.set_state(ConfirmRegistration.confirm_record)


@router.message(ConfirmRegistration.confirm_record, F.text)
async def recording_client(message: Message, state: FSMContext, bot: Bot):
    data_record = dict_from_message(message.text)
    await bot.send_message(data_record['ID'], text=f'Ваша запись ПОДТВЕРЖДЕНА!\n\n'
                                                   f'Ждем вас {data_record["Число"]} в {data_record["Время"]}\n'
                                                   f'Будем делать Ра-та-та')
    await message.answer(text=f'Запись на {data_record["Число"]} в {data_record["Время"]} подтверждена')
    await state.clear()


@router.message(Command('happy_birthday'))
async def happy_birthday(message: Message, session_maker: sessionmaker):
    today = date.today()
    future = today + timedelta(days=7)
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(select(Staff).filter(
                extract('month', Staff.birth_date).between(today.month, future.month),
                extract('day', Staff.birth_date).between(today.day, future.day)
            ))
            birthday_employers = result.scalars()
    if birthday_employers:
        happy_list = '\n'.join([f'{employer.first_name} {employer.surname} - {employer.position} '
                                f'ДР: {employer.birth_date.day}.{employer.birth_date.month}'
                                for employer in birthday_employers])
        await message.answer(text=f'Ближайшие именинники:\n {happy_list}')
    else:
        await message.answer(text='Ближайшие семь дней нет именинников')
