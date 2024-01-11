from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton, InlineKeyboardBuilder

from core.lexicon.lexicon_ru import LEXICON_EDIT_EMPLOYER


def confirm_adding_employer_keyboard() -> InlineKeyboardMarkup:
    col = [
        [InlineKeyboardButton(text='Да', callback_data='yes')],
        [InlineKeyboardButton(text='Нет', callback_data='no')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=col)


def edit_employer_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for param, callback in LEXICON_EDIT_EMPLOYER.items():
        builder.add(InlineKeyboardButton(text=param, callback_data=callback))
    builder.adjust(1)
    return builder.as_markup()


def choose_edit_employer_keyboard() -> InlineKeyboardMarkup:
    col = [
        [InlineKeyboardButton(text='Изменить', callback_data='change')],
        [InlineKeyboardButton(text='Удалить', callback_data='delete')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=col)
