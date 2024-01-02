from aiogram import Router, F, Bot
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from core.settings import settings

router = Router()


async def start_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text='Бот завелся!')


async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text='Бот заглох!')


@router.message(Command('start'))
async def get_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text=f'Приветствуем {message.from_user.full_name}!',
                         reply_markup=ReplyKeyboardRemove())


@router.message(Command('cancel'))
@router.message(F.text == 'Отмена' or F.text == 'отмена')
async def action_cancel(message: Message, state: FSMContext):
    await state.clear()
    await state.set_data({})
    await message.answer(text='Действие отменено',
                         reply_markup=ReplyKeyboardRemove())
