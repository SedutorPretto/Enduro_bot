from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup, KeyboardButton
from core.lexicon.lexicon_ru import AVAILABLE_MONTHS, MOTOBIKES, INSTRUCTORS


def month_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for month in AVAILABLE_MONTHS:
        builder.add(KeyboardButton(text=month))
    builder.adjust(4)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def time_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for i in range(9, 19):
        builder.add(KeyboardButton(text=f'{str(i)}:00'))
        if i < 18:
            builder.add(KeyboardButton(text=f'{str(i)}:30'))
    builder.adjust(5)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def service_keyboard() -> ReplyKeyboardMarkup:
    row = [KeyboardButton(text=el) for el in ['Площадка', 'Рельеф', 'Тур']]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True, one_time_keyboard=True)


def instructors_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for ins in INSTRUCTORS:
        builder.add(KeyboardButton(text=ins))
    builder.adjust(3)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def moto_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for moto in MOTOBIKES:
        builder.add(KeyboardButton(text=moto))
    builder.adjust(3)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def comment_keyboard() -> ReplyKeyboardMarkup:
    col = [KeyboardButton(text='Пропустить')]
    return ReplyKeyboardMarkup(keyboard=[col], resize_keyboard=True, one_time_keyboard=True)


def finish_keyboard() -> ReplyKeyboardMarkup:
    col = [
        [KeyboardButton(text='Записаться')],
        [KeyboardButton(text='Изменить запись')]
    ]
    return ReplyKeyboardMarkup(keyboard=col, resize_keyboard=True, one_time_keyboard=True)