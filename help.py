from datetime import datetime
from aiogram import Bot, Dispatcher
import json
import os


def next_day(today: str) -> str:
    """Count next day"""
    # НЕпонятно, что несмотря на то, что
    # Словари неупорядоченные отображения. Возвращаемы json.load() словари упорядочиваемы
    today_index = DAYS_EN.index(today)
    tomorrow_index = today_index + 1
    if tomorrow_index > 6:
        tomorrow_index = 0
    tomorrow_en = DAYS_EN[tomorrow_index]
    return tomorrow_en


def open_json(filename) -> str:
    """Открывает json файл для чтения и возвращает его как словарь"""
    with open(filename, encoding='utf-8') as file:
        data = json.load(file)
    return data


def read_by_key(obj, *keys: str) -> str:
    """Возвращает расписание на день"""
    result = ''
    # referring to days of week
    for key in keys:
        day_shedule = obj[key]
        # referring to shedule order
        for i in day_shedule:
            subject = day_shedule[i]
            # subject = subject[:10] + f'<b>{subject[10:15]}</b>' + subject[15:]
            result += day_shedule[i]
            # result = subject

    return result


def is_id_in(obj: str, id: str) -> bool:
    """Возваращает True, если id нет в файле, иначе False"""
    with open(obj) as file:
        text = file.read()
        if id in text:
            # есть в файле
            return True
        else:
            # Не в файле
            file.close()
            return False


def get_ids(obj):
    """Получает все айди"""
    with open(obj) as file:
        ids = file.read()
    result = ids.split('\n')
    result = [i for i in result if i]
    return result


def get_current_datetime() -> tuple:
    """Получает текующие день недели и дату"""
    result = datetime.now().ctime()
    split_ = result.split()
    day, time = split_[0], split_[3]
    return day, time


def write_id(obj: str, id: str):
    """Записывает id, если его ранее не было"""
    try:
        if not is_id_in(obj, id):
            with open(obj, 'a') as file:
                file.write(id + '\n')
        return True
    except Exception as ex:
        return 'Id не записан. Ошибка:', ex


API_TOKEN = os.environ["TG_TOKEN"]
DAYS_EN = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
DAYS_RUS = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
TRANSLATOR = dict(zip(DAYS_EN, DAYS_RUS))

# initialize bot
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
