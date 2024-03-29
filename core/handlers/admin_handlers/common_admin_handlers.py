from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

from core.utils.admin import dict_from_message
from core.handlers.states import ConfirmRegistration


router = Router()


@router.message(Command('confirm_record'))
@router.message(F.text.lower() == 'подтвердить регистрацию')
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
@router.message(F.text.lower() == 'предстоящие дни рождения')
async def happy_birthday(message: Message, session_maker: sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            query = text("""
            SELECT *
            FROM employers
            WHERE MAKE_DATE(EXTRACT(YEAR FROM CURRENT_DATE)::INT, 
                            EXTRACT(MONTH FROM birth_date)::INT, 
                            EXTRACT(DAY FROM birth_date)::INT) 
            BETWEEN CURRENT_DATE AND CURRENT_DATE + 7
            """)
            result = await session.execute(query)
            birthday_employers = result.fetchall()
    if birthday_employers:
        happy_list = '\n'.join([f'{employer.first_name} {employer.surname} - {employer.position} '
                                f'ДР: {employer.birth_date.day}.{employer.birth_date.month}'
                                for employer in birthday_employers])
        await message.answer(text=f'Ближайшие именинники:\n {happy_list}')
    else:
        await message.answer(text='Ближайшие семь дней нет именинников')
