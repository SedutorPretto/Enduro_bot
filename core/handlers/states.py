from aiogram.fsm.state import State, StatesGroup


class FSMRegistrationTrip(StatesGroup):
    choosing_month = State()
    choosing_day = State()
    choosing_time = State()
    choosing_service = State()
    choosing_instructor = State()
    choosing_moto = State()
    adding_phone = State()
    adding_comments = State()
    finish_state = State()


class FSMConfirmRegistration(StatesGroup):
    confirm_record = State()


class FSMCallback(StatesGroup):
    confirm_contact = State()


class FSMAddEmployer(StatesGroup):
    add_name = State()
    add_surname = State()
    add_phone = State()
    add_birthdate = State()
    add_position = State()
    add_photo = State()
    editing_employer = State()
    confirm_state = State()


class FSMRUDEmployer(StatesGroup):
    receive_name = State()
    receive_id = State()
    choose_edit_employer = State()
    update_employer = State()
    finish_state = State()
