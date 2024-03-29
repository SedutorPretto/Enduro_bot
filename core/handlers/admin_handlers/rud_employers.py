from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from core.handlers.states import FSMRUDEmployer
from core.database.models import Staff
from core.keyboards.CRUD_employer import choose_edit_employer_keyboard, edit_employer_keyboard

router = Router()


@router.message(Command('change_instructor'))
@router.message(F.text.lower() == 'удалить/изменить инструктора')
async def receive_name(message: Message, state: FSMContext):
    await message.answer(text='Введи Имя сотрудника, которого хочешь изменить')
    await state.set_state(FSMRUDEmployer.receive_name)


@router.message(FSMRUDEmployer.receive_name)
async def receive_employers(message: Message, state: FSMContext, session_maker: sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(select(Staff).filter(Staff.first_name == message.text))
            staff_instance = result.scalars()
        if staff_instance:
            res = '\n'.join([f'ID:{staff.user_id} - {staff.first_name} {staff.surname} - {staff.position}'
                             for staff in staff_instance])
            await message.answer(text=f'{res}\n'
                                      f'Введи ID сотрудника которого хочешь изменить')
            await state.set_state(FSMRUDEmployer.receive_id)
        else:
            await message.answer(text='Такого сотрудника не существует\n '
                                      'Введи Имя сотрудника, которого хочешь изменить')


@router.message(FSMRUDEmployer.receive_id)
async def chose_employer(message: Message, state: FSMContext):
    await state.update_data(id=int(message.text))
    await message.answer(text='Что хочешь сделать с сотрудником?',
                         reply_markup=choose_edit_employer_keyboard())
    await state.set_state(FSMRUDEmployer.choose_edit_employer)


@router.callback_query(FSMRUDEmployer.choose_edit_employer, F.data == 'delete')
async def delete_employer(callback: CallbackQuery, state: FSMContext, session_maker: sessionmaker):
    user_data = await state.get_data()
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(select(Staff).filter(Staff.user_id == user_data['id']))
            employer = result.scalar()
            await session.delete(employer)
            await session.commit()

    await callback.answer(
        text='Cотрудник удален!',
        show_alert=True
    )
    await state.clear()
    await state.set_data({})


@router.callback_query(FSMRUDEmployer.choose_edit_employer, F.data == 'change')
async def update_employer(callback: CallbackQuery, state: FSMContext, session_maker: sessionmaker):
    user_data = await state.get_data()
    await callback.message.delete()
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(select(Staff).filter(Staff.user_id == user_data['id']))
            employer = result.scalar()
            await callback.message.answer_photo(employer.telegram_photo,
                                                caption=f'{employer.first_name} {employer.surname}\n'
                                                        f'{employer.phone_number}\n'
                                                        f'{employer.birth_date}\n'
                                                        f'{employer.position}',
                                                reply_markup=edit_employer_keyboard())
    await state.set_state(FSMRUDEmployer.update_employer)


@router.callback_query(FSMRUDEmployer.update_employer, F.data == 'telegram_photo')
async def update_photo(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text='Пришли новое фото')
    await state.set_state(FSMRUDEmployer.finish_state)


@router.callback_query(FSMRUDEmployer.update_employer)
async def update_field(callback: CallbackQuery, state: FSMContext):
    await state.update_data(upd=callback.data)
    await callback.message.answer(text='Введи новое значение')
    await state.set_state(FSMRUDEmployer.finish_state)


@router.message(FSMRUDEmployer.finish_state, F.photo)
async def new_photo(message: Message, session_maker: sessionmaker, state: FSMContext):
    user_data = await state.get_data()
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(select(Staff).filter(Staff.user_id == user_data['id']))
            employer = result.scalar()
            employer.telegram_photo = message.photo[-1].file_id
            await session.commit()

    await message.answer(text='Фото обновлено')
    await state.clear()
    await state.set_data({})


@router.message(FSMRUDEmployer.finish_state, F.text)
async def finish_update_field(message: Message, session_maker: sessionmaker, state: FSMContext):
    user_data = await state.get_data()
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(select(Staff).filter(Staff.user_id == user_data['id']))
            employer = result.scalar()
            setattr(employer, user_data['upd'], message.text)
            await session.commit()

    await message.answer(text='Изменение сохранено')
    await state.clear()
    await state.set_data({})
