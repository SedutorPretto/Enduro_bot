from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from core.utils.admin import dict_from_message
from core.handlers.states import ConfirmRegistration
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
