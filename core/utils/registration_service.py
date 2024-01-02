from datetime import datetime
from calendar import monthrange, weekday


from core.lexicon.lexicon_ru import AVAILABLE_MONTHS


def max_days_in_month(month):
    current_year = datetime.now().year
    days = monthrange(current_year, AVAILABLE_MONTHS[month])
    return days[1]


def day_name(month, day):
    day_names = {0: 'Понедельник',
                 1: 'Вторник',
                 2: 'Среда',
                 3: 'Четверг',
                 4: 'Пятница',
                 5: 'Суббота',
                 6: 'Воскресенье'}
    year = datetime.now().year
    return day_names[weekday(year, AVAILABLE_MONTHS[month], int(day))]
