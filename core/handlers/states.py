from aiogram.fsm.state import State, StatesGroup


class RegistrationTrip(StatesGroup):
    choosing_month = State()
    choosing_day = State()
    choosing_time = State()
    choosing_service = State()
    choosing_instructor = State()
    choosing_moto = State()
    adding_comments = State()
    finish_state = State()

class ConfirmRegistration(StatesGroup):
    confirm_record = State()
