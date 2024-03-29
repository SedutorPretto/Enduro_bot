from datetime import date
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from sqlalchemy.orm import sessionmaker

from core.database.models import Staff
from core.handlers.states import FSMAddEmployer
from core.keyboards.CRUD_employer import confirm_adding_employer_keyboard
from core.filters.admin_filters import CorrectData, CorrectPhone
from core.lexicon.add_employer import ADD_NAME, ADD_PHONE, ADD_PHOTO, ADD_SURNAME, NEW_EMPLOYER, \
                                      ADD_POSITION, ADD_BIRTHDATE, ERROR_PHONE, ERROR_BIRTHDATE, RESTART

router = Router()


@router.message(Command('add_employer'))
@router.message(F.text.lower() == 'добавить инструктора')
async def add_employer(message: Message, state: FSMContext):
    await message.answer(text=ADD_NAME)
    await state.set_state(FSMAddEmployer.add_name)


@router.message(FSMAddEmployer.add_name)
async def added_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(text=ADD_SURNAME)
    await state.set_state(FSMAddEmployer.add_surname)


@router.message(FSMAddEmployer.add_surname)
async def added_surname(message: Message, state: FSMContext):
    await state.update_data(surname=message.text)
    await message.answer(text=ADD_PHONE)
    await state.set_state(FSMAddEmployer.add_phone)


@router.message(FSMAddEmployer.add_phone, CorrectPhone())
async def added_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer(text=ADD_BIRTHDATE)
    await state.set_state(FSMAddEmployer.add_birthdate)


@router.message(FSMAddEmployer.add_phone)
async def wrong_added_phone(message: Message):
    await message.answer(text=ERROR_PHONE)


@router.message(FSMAddEmployer.add_birthdate, CorrectData())
async def added_birthdate(message: Message, state: FSMContext):
    await state.update_data(birth_date=message.text)
    await message.answer(text=ADD_POSITION)
    await state.set_state(FSMAddEmployer.add_position)


@router.message(FSMAddEmployer.add_birthdate)
async def wrong_added_birthdate(message: Message):
    await message.answer(text=ERROR_BIRTHDATE)


@router.message(FSMAddEmployer.add_position)
async def added_position(message: Message, state: FSMContext):
    await state.update_data(position=message.text)
    await message.answer(text=ADD_PHOTO)
    await state.set_state(FSMAddEmployer.add_photo)


@router.message(FSMAddEmployer.add_photo, F.photo)
async def added_photo(message: Message, state: FSMContext):
    await state.update_data(photo=message.photo[-1].file_id)
    user_data = await state.get_data()
    await message.answer_photo(user_data['photo'],
                               caption=f'{user_data["name"]} {user_data["surname"]}\n'
                                       f'{user_data["phone"]}\n'
                                       f'{user_data["birth_date"]}\n'
                                       f'{user_data["position"]}\n')
    await message.answer(text='Все верно?',
                         reply_markup=confirm_adding_employer_keyboard())
    await state.set_state(FSMAddEmployer.confirm_state)


@router.callback_query(FSMAddEmployer.confirm_state, F.data == 'yes')
async def added_employer(callback: CallbackQuery, state: FSMContext, session_maker: sessionmaker):
    user_data = await state.get_data()
    async with session_maker() as session:
        async with session.begin():
            employer = Staff(first_name=user_data["name"],
                             surname=user_data["surname"],
                             phone_number=user_data["phone"],
                             birth_date=date.fromisoformat(user_data["birth_date"]),
                             position=user_data["position"],
                             telegram_photo=user_data['photo'])
            session.add(employer)
            await session.flush()
            await session.commit()

    await callback.answer(
        text=NEW_EMPLOYER,
        show_alert=True
    )
    await state.clear()
    await state.set_data({})


@router.callback_query(FSMAddEmployer.confirm_state, F.data == 'no')
async def edit_employer(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=RESTART)
    await state.set_state(FSMAddEmployer.add_name)
