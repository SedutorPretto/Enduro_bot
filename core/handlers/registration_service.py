from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command

from core.handlers.states import RegistrationTrip
from core.keyboards.registration_service import month_keyboard, time_keyboard, \
    service_keyboard, instructors_keyboard, moto_keyboard, comment_keyboard, finish_keyboard
from core.settings import settings
from core.utils.registration_service import max_days_in_month, day_name
from core.lexicon.lexicon_ru import AVAILABLE_MONTHS, MOTOBIKES, INSTRUCTORS, SERVICES
from core.filters.registration_service import ChooseDay, ChooseTime

router = Router()


@router.message(Command('registration_trip'))
async def service_registration(message: Message, state: FSMContext):
    await message.answer(text='Выберите месяц на который хотите записаться:',
                         reply_markup=month_keyboard())
    await state.set_state(RegistrationTrip.choosing_month)


@router.message(RegistrationTrip.choosing_month, F.text.in_(AVAILABLE_MONTHS))
async def month_chosen(message: Message, state: FSMContext):
    # Выбор месяца корректный
    await state.update_data(month=message.text)
    await state.update_data(max_days=max_days_in_month(message.text))
    await message.answer(
        text='Ввведите число на которое хотите записаться:')
    # todo сделать чтобы в строке ввода тоже писалось про число
    await state.set_state(RegistrationTrip.choosing_day)


@router.message(RegistrationTrip.choosing_month)
async def wrong_month_chosen(message: Message):
    await message.reply(text='Какой-то неизвестный месяц\n\n'
                             'Выберите месяц на который хотите записаться ниже:',
                        reply_markup=month_keyboard())


@router.message(RegistrationTrip.choosing_day, ChooseDay())
async def day_chosen(message: Message, state: FSMContext):
    user_data = await state.get_data()
    day_name_rus = day_name(user_data["month"], message.text)
    await state.update_data(day=message.text, day_name=day_name_rus)
    await message.answer(text='Мы работаем с 9 до 19\n\n'
                              'Выберите время на которое хотите записаться',
                         reply_markup=time_keyboard())
    await state.set_state(RegistrationTrip.choosing_time)


@router.message(RegistrationTrip.choosing_day)
async def wrong_day_chosen(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await message.reply(text=f'Напишите число цифрами, в этом месяце {user_data["max_days"]} дней\n\n'
                             'Введите число на которое хотите записаться:')  # todo добавить функцию форматирования день\дня\дней


@router.message(RegistrationTrip.choosing_time, ChooseTime())
async def time_chosen(message: Message, state: FSMContext):
    await state.update_data(time=message.text)
    await message.answer(text='Выберите куда вы хотите поехать:',
                         reply_markup=service_keyboard())
    await state.set_state(RegistrationTrip.choosing_service)


@router.message(RegistrationTrip.choosing_time)
async def wrong_time_chosen(message: Message):
    await message.reply(text='На это время нельзя записаться\n\n'
                             'Выберите время из доступного:')


@router.message(RegistrationTrip.choosing_service, F.text.in_(SERVICES))
async def service_chosen(message: Message, state: FSMContext):
    await state.update_data(service=message.text)
    await message.answer(text='Выберите инструктора:',
                         reply_markup=instructors_keyboard())
    await state.set_state(RegistrationTrip.choosing_instructor)


@router.message(RegistrationTrip.choosing_service)
async def wrong_service_chosen(message: Message):
    await message.reply(text='На такую услугу нельзя записаться через бота\n\n'
                             'Выберите из представленных или свяжитесь с нами:')
        # todo вставить телефон чтоб можно было сразу звонить


@router.message(RegistrationTrip.choosing_instructor, F.text.in_(INSTRUCTORS))
async def instructor_chosen(message: Message, state: FSMContext):
    await state.update_data(instructor=message.text)
    await message.answer(text='Выберите мотоцикл',
                         reply_markup=moto_keyboard())
    await state.set_state(RegistrationTrip.choosing_moto)


@router.message(RegistrationTrip.choosing_instructor)
async def wrong_instructor_chosen(message: Message):
    await message.reply(text='Такого инструктора в этот день у нас нет\n\n'
                             'Выберите инструктора:')


@router.message(RegistrationTrip.choosing_moto, F.text.in_(MOTOBIKES))
async def moto_chosen(message: Message, state: FSMContext):
    await state.update_data(moto=message.text)
    await message.answer(
        text='Напишите комментарии если необходимо или нажмите "Пропустить"',
        reply_markup=comment_keyboard())
    await state.set_state(RegistrationTrip.adding_comments)


@router.message(RegistrationTrip.choosing_moto)
async def wrong_moto_chosen(message: Message):
    await message.reply(text='Такого мотоцикла в этот день у нас нет\n\n'
                             'Выберите другой:')


@router.message(RegistrationTrip.adding_comments)
async def add_comment(message: Message, state: FSMContext):
    if message.text == 'Пропустить':
        comment = ''
    else:
        comment = message.text
    await state.update_data(comment=comment)
    user_data = await state.get_data()
    await message.answer(
        text=f'Давайте проверим. Вы xотите записаться:\n'
             f'Число: {user_data["month"]} {user_data["day"]} это {user_data["day_name"]}\n'
             f'Время: {user_data["time"]}\n'
             f'Услуга: {user_data["service"]}\n'
             f'Инструктор: {user_data["instructor"]}\n'
             f'Мотоцикл: {user_data["moto"]}\n'
             f'Комментарий: {user_data["comment"]}\n'
             f'Все верно?',
        reply_markup=finish_keyboard()
    )
    await state.set_state(RegistrationTrip.finish_state)


@router.message(RegistrationTrip.finish_state, F.text == 'Записаться')
async def finish_registration(message: Message, state: FSMContext, bot: Bot):
    user_data = await state.get_data()
    # day = day_name(user_data["month"], user_data["day"])   todo костыль, заменить
    await message.answer(text='Ожидайте подверждения',
                         reply_markup=ReplyKeyboardRemove())
    await bot.send_message(settings.bots.admin_id,
                           text=f'Имя- {message.from_user.full_name}\n'
                                f'ID- {message.from_user.id}\n'
                                f'Ник- {message.from_user.username}\n'
                                f'Число- {user_data["month"]} {user_data["day"]} это {user_data["day_name"]}\n'
                                f'Время- {user_data["time"]}\n'
                                f'Услуга- {user_data["service"]}\n'
                                f'Инструктор- {user_data["instructor"]}\n'
                                f'Мотоцикл- {user_data["moto"]}\n'
                                f'Комментарий- {user_data["comment"]}\n')
    await state.clear()
    await state.set_data({})


@router.message(RegistrationTrip.finish_state, F.text == 'Изменить запись')
async def another_registration(message: Message, state: FSMContext):
    await state.set_data({})
    await state.clear()
    await service_registration(message, state)


@router.message(RegistrationTrip.finish_state)
async def finish_registration_incorrect(message: Message):
    await message.answer(text='Пожалуйста нажмите на одну из кнопок ниже:',
                         reply_markup=finish_keyboard())
