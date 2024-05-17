from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

from core.settings import settings
from core.keyboards.base_menu import base_client_keyboard, base_admin_keyboard
from core.lexicon.lexicon_ru import LEXICON_HELP_ADMIN, LEXICON_HELP_CLIENT

router = Router()


async def start_bot(bot: Bot):
    await bot.send_message(settings.tg_bot.admin_id, text='Бот завелся!')


async def stop_bot(bot: Bot):
    await bot.send_message(settings.tg_bot.admin_id, text='Бот заглох!')


@router.message(CommandStart())
async def get_start(message: Message, state: FSMContext, admin_check):
    await state.clear()
    if admin_check:
        await message.answer(text=f'Приветствуем {message.from_user.full_name}!',
                             reply_markup=base_admin_keyboard())
    else:
        await message.answer(text=f'Приветствуем {message.from_user.full_name}!',
                             reply_markup=base_client_keyboard())




@router.message(Command('cancel'))
@router.message(F.text.lower() == 'отмена')
async def action_cancel(message: Message, state: FSMContext, admin_check):
    await state.clear()
    await state.set_data({})
    if admin_check:
        await message.answer(text='Действие отменено',
                             reply_markup=base_admin_keyboard())
    else:
        await message.answer(text='Действие отменено',
                             reply_markup=base_client_keyboard())


@router.message(Command('help'))
async def helper(message: Message, admin_check):
    if admin_check:
        await message.answer(text=LEXICON_HELP_ADMIN,
                             reply_markup=base_admin_keyboard())
    else:
        await message.answer(text=LEXICON_HELP_CLIENT,
                             reply_markup=base_client_keyboard())
