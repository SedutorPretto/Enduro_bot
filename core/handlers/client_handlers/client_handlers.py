from aiogram import Router, F, Bot
from aiogram.types import Message, Contact
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from core.database.models import Staff
from core.handlers.states import FSMCallback
from core.filters.admin_filters import CorrectPhone
from core.lexicon.lexicon_ru import LEXICON_CALLBACK, LEXICON_CONTACTS
from core.settings import settings

router = Router()


@router.message(Command('instructors'))
@router.message(F.text.lower() == 'лучшие инструктора')
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
    await message.answer(text=LEXICON_CONTACTS,
                         disable_web_page_preview=True)


@router.message(Command('call_me'))
@router.message(F.text.lower() == 'Обратный звонок')
async def callback_view_1(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_CALLBACK)
    await state.set_state(FSMCallback.confirm_contact)


@router.message(FSMCallback.confirm_contact, CorrectPhone())
async def callback_view_2(message: Message, state: FSMContext, bot: Bot):
    await bot.send_message(settings.tg_bot.admin_id, text=f'{message.from_user.full_name}\n\n'
                                                          f'{message.text}\n\n'
                                                          f'Просит позвонить!')
    await message.answer(text='Мы наберем вас в ближайшее время')
    await state.clear()


@router.message(F.contact)
async def callback_contact_view(message: Message, bot: Bot):
    await message.answer(text='Мы свяжемся с вами в ближайшее время!')
    await bot.send_contact(settings.tg_bot.admin_id, message.contact.phone_number, message.contact.first_name)


@router.message(FSMCallback.confirm_contact)
async def callback_view_wrong(message: Message):
    await message.answer(text='Пожалуйста введите корректный номер телефона в формате: \n\n'
                              '+79ХХХХХХХХХ')
