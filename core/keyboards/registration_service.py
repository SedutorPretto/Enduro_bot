from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup, KeyboardButton
from sqlalchemy import select

from core.database.models import Staff
from core.lexicon.lexicon_ru import AVAILABLE_MONTHS, MOTOBIKES, SERVICES


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
    row = [KeyboardButton(text=el) for el in SERVICES]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True, one_time_keyboard=True)


async def instructors_keyboard(session_maker) -> ReplyKeyboardMarkup:
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(select(Staff).filter(Staff.position == 'инструктор'))
            instructors = result.scalars()
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text='Не важно, главное чтоб классный'))
    for ins in instructors:
        try:
            builder.add(KeyboardButton(text=ins.first_name))
        except AttributeError:
            pass
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
