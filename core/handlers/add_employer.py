from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import Message


from core.handlers.states import AddEmployer

router = Router()


# todo добавить ожидаемые форматы чтобы админу было проще
@router.message(Command('add_employer'))
async def add_employer(message: Message, state: FSMContext):
    await message.answer(text='Введи имя сотрудника на русском')
    await state.set_state(AddEmployer.add_name)


@router.message(AddEmployer.add_name)
async def added_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(text='Теперь введи фамилию')
    await state.set_state(AddEmployer.add_surname)


@router.message(AddEmployer.add_surname)
async def added_surname(message: Message, state: FSMContext):
    await state.update_data(surname=message.text)
    await message.answer(text='Теперь введи номер телефона')
    await state.set_state(AddEmployer.add_phone)


@router.message(AddEmployer.add_phone)
async def added_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer(text='Теперь введи дату рождения')
    await state.set_state(AddEmployer.add_birthdate)


@router.message(AddEmployer.add_birthdate)
async def added_birthdate(message: Message, state: FSMContext):
    await state.update_data(birthdate=message.text)
    await message.answer(text='Теперь введи должность')  # todo сделать список должностей
    await state.set_state(AddEmployer.add_position)


@router.message(AddEmployer.add_position)
async def added_position(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer(text='Теперь отправь фото')
    await state.set_state(AddEmployer.add_photo)
