from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup, KeyboardButton
from core.lexicon.lexicon_ru import LEXICON_COMMANDS_CLIENT, LEXICON_COMMANDS_ADMIN


def base_client_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for item in LEXICON_COMMANDS_CLIENT:
        builder.add(KeyboardButton(text=item))
    builder.add(KeyboardButton(text='Обратный звонок',
                               request_contact=True))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def base_admin_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for item in LEXICON_COMMANDS_ADMIN:
        builder.add(KeyboardButton(text=item))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)
