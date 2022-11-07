from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

# Кнопки на панели пользователя
user_bttn_week = KeyboardButton(text="Сегодня")
user_bttn_today = KeyboardButton(text='Завтра')
user_bttn_tomrw = KeyboardButton(text="Неделя")
reply_bttns = ReplyKeyboardMarkup(resize_keyboard=True)
reply_bttns.add(user_bttn_tomrw).add(user_bttn_week).add(user_bttn_today)

# Кнопки при вызове недель
week1_bttn = InlineKeyboardButton(text='1-я неделя', callback_data='Неделя 1')
week2_bttn = InlineKeyboardButton(text=f'2-я неделя', callback_data='Неделя 2')
weeks_kb = InlineKeyboardMarkup().add(week1_bttn).add(week2_bttn)
