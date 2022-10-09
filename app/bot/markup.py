import os
from telebot import types
from dotenv import load_dotenv

config = load_dotenv()
off_markup = types.ReplyKeyboardRemove(selective=False)
role_msg = 'Привет! Выбери свою роль'

role = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
itembtn1 = types.KeyboardButton('Директор')
itembtn2 = types.KeyboardButton('Бухгалтер')
role.add(itembtn1,itembtn2)

scope_of_activity_msg = 'Выбери сферу деятельности!'
scope_of_activity = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
itembtn1 = types.KeyboardButton('сельское хозяйство')
itembtn2 = types.KeyboardButton('банковский сектор')
itembtn3 = types.KeyboardButton('гос управление')
itembtn4 = types.KeyboardButton('топливная промышленность')
itembtn5 = types.KeyboardButton('военная отрасль')
itembtn6 = types.KeyboardButton('финансовый сектор')
scope_of_activity.add(itembtn1,itembtn2,itembtn3,itembtn4,itembtn5,itembtn6)

menu_msg = 'Здесь только отборные новости!'
menu_mp = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
itembtn1 = types.KeyboardButton('/Дайджест')
itembtn2 = types.KeyboardButton('/Новости')
menu_mp.add(itembtn1,itembtn2)
