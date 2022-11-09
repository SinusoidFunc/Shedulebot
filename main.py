import logging
from aiogram import executor, types
from help import *
from keyboard import reply_bttns, weeks_kb
import datetime
import asyncio

# Загрузка расписания
with open("shedule_1.json", encoding='utf-8') as file:
    WEEK1_SHEDULE = json.load(file)

with open("shedule_2.json", encoding='utf-8') as file:
    WEEK2_SHEDULE = json.load(file)

# configure logging
logging.basicConfig(level=logging.INFO)


async def send_sheduled_mess(time):  # time format = '07:35:02'
    """Отправляет расписание на текущий день user_id, если наступил time"""

    while True:
        ids = get_ids('id.txt')
        curr_day, curr_time = get_current_datetime()
        for id in ids:
            if curr_time == time:
                logging.info("Высылаю расписание на установленное время!")
                await bot.send_message(id, create_send_mess(curr_day), parse_mode='HTML')
        await asyncio.sleep(1)


# Чтобы не использовать importlib.reload()
def choose_shedule():
    """Выбирает расписание."""
    if int(datetime.datetime.today().strftime("%W")) % 2 != 0:
        return WEEK1_SHEDULE
    else:
        return WEEK2_SHEDULE


# Эта функция здесь, а не в help.py, т.к
# Мне придется постоянно обновлять week_number, а help.py я импортирую только один раз
# Поэтому сколько бы не менял там SHEDULE_DATA в данном файле он не будет обновляться
# Поэтому вычисление SHEDULE_DATA я буду выполнять сдесь
def create_send_mess(day_en: str, day='Сегодня') -> str:
    """Создает сообщения для выбранного дня недели"""
    shedule_data = choose_shedule()
    sending_message = ''
    day_of_week_rus = TRANSLATOR[day_en]
    sending_message = f'{"=" * len(day_of_week_rus)}\n{day} - {day_of_week_rus}\n'
    sending_message += read_by_key(shedule_data, day_en)
    sending_message += '=' * len(day_of_week_rus)
    return sending_message


@dp.message_handler(commands=['start'])
async def greeting_message(message: types.Message):
    await bot.send_message(message.from_id,
                           'Привет, я покажу тебе твое расписание.\n'
                           'Выбери соответствующий пункт!',
                           reply_markup=reply_bttns)


@dp.message_handler(commands=['help'])
async def help_message(message: types.Message):
    await bot.send_message(message.from_id,
                           'Выбери соответствующий твоим запросам пункт.')


@dp.message_handler(commands=['today'])
@dp.message_handler(text='Сегодня')
async def today(message: types.Message):
    """Отправляет пользователю расписание на текущий день."""
    day_of_week = datetime.date.today().ctime()[:3]
    sending_message = create_send_mess(day_of_week, day='Сегодня')
    await bot.send_message(message.from_id, sending_message, parse_mode='HTML')


@dp.message_handler(commands=['tomorrow'])
@dp.message_handler(text='Завтра')
async def tomorrow(message: types.Message):
    """Send the shedule of the next day."""
    logging.info('Отправляю расписание')
    tomorrow_en = next_day(datetime.date.today().ctime()[:3])
    tomorrow_rus = TRANSLATOR[tomorrow_en]
    sending_message = create_send_mess(tomorrow_en, day='Завтра')
    await bot.send_message(message.from_id, sending_message, parse_mode='HTML')


@dp.message_handler(commands=['week'])
@dp.message_handler(text='Неделя')
async def week(message: types.Message):
    logging.info('Отправляю расписание')
    await message.answer('Выбери неделю:', reply_markup=weeks_kb)


@dp.callback_query_handler(text='Неделя 1')
async def callback_reg1(callback: types.CallbackQuery):
    sending_message = 'Расписание на 1-ю неделю\n\n'
    opened_json = open_json('shedule_1.json')
    for i in opened_json:
        sending_message += TRANSLATOR[i] + '\n'
        sending_message += read_by_key(opened_json, i)
        sending_message += '======\n'
    await callback.message.answer(text=sending_message, parse_mode='HTML')


@dp.callback_query_handler(text='Неделя 2')
async def callback_reg2(callback: types.CallbackQuery):
    sending_message = 'Расписание на 2-ю неделю\n\n'
    opened_json = open_json('shedule_2.json')
    for i in opened_json:
        sending_message += TRANSLATOR[i] + '\n'
        sending_message += read_by_key(opened_json, i)
        sending_message += '======\n'
    await callback.message.answer(text=sending_message, parse_mode='HTML')


@dp.message_handler(commands=['week_1', 'week_2'])
async def show_week_shedule(message: types.Message):
    logging.info('Отправляю расписание')
    sending_message = ''
    if message.text == '/week_1':
        opened_json = open_json('shedule_1.json')
    else:
        opened_json = open_json('shedule_2.json')
    for i in opened_json:
        sending_message += TRANSLATOR[i] + '\n'
        sending_message += read_by_key(opened_json, i)
        sending_message += '======\n'
    await message.answer(text=sending_message, parse_mode='HTML')


@dp.message_handler()
async def answer(message: types.Message):
    logging.info(f'Непонятный запрос: message - {message.text}: id - {message.from_id}')
    await message.answer('<b>Непонятный запрос</b>', parse_mode='HTML')


def main():
    logging.info('Запускаю бота!')
    loop = asyncio.get_event_loop()
    loop.create_task((send_sheduled_mess(time='18:23:30')))
    executor.start_polling(dp, loop=loop)


if __name__ == '__main__':
    main()
