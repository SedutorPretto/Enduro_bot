from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message


class ChooseDay(BaseFilter):
    async def __call__(self, message: Message, state: FSMContext):
        user_data = await state.get_data()
        max_day = int(user_data['max_days'])
        try:
            return 1 <= int(message.text) <= max_day
        except ValueError:
            return False


class ChooseTime(BaseFilter):
    async def __call__(self, message: Message):
        hours, minutes = message.text.split(':')
        return 9 <= int(hours) < 19 and (minutes in ('00', '30'))
