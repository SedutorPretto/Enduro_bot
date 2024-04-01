from re import match
from datetime import datetime

from aiogram.filters import BaseFilter
from aiogram.types import Message


class CorrectData(BaseFilter):
    async def __call__(self, message: Message):
        try:
            datetime.strptime(message.text, '%Y-%m-%d')
            return True
        except ValueError:
            return False


class CorrectPhone(BaseFilter):
    async def __call__(self, message: Message):
        return bool(match(r'^\+79\d{9}$', message.text))
