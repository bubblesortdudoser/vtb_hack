import os
import telebot
from telebot import types
import markup as mp
from dotenv import load_dotenv

config = load_dotenv()
bot = telebot.TeleBot(os.getenv("TG_API_KEY"))

users = dict()

@bot.message_handler(commands=['start'])
def start(message) -> None:
    try:
        users[message.chat.id] = {"role": '', "scope_of_activity": '', "category": ''}
        msg = bot.send_message(message.chat.id, mp.role_msg, reply_markup=mp.role, parse_mode='MARKDOWN')
        bot.register_next_step_handler(msg, role)

    except Exception as e:
        bot.reply_to(message, f'{e}')

def role(message):
    try:
        users[message.chat.id]["role"] = message.text
        msg = bot.send_message(message.chat.id, mp.scope_of_activity_msg, reply_markup=mp.scope_of_activity, parse_mode='MARKDOWN')
        bot.register_next_step_handler(msg, scope_of_activity)
    except Exception as e:
        bot.reply_to(message, f'{e}')

def scope_of_activity(message):
    try:
        users[message.chat.id]["scope_of_activity"] = message.text
        bot.send_message(message.chat.id, mp.menu_msg, reply_markup=mp.menu_mp, parse_mode='MARKDOWN')
        users[message.chat.id]["category"] = None
    except Exception as e:
        bot.reply_to(message, f'{e}')

@bot.message_handler(commands=['дайджест'])
def start(message) -> None:
    try:
        msg = '''
Дайджест!
1) Новость1
2) Новость2
3) Новость3
4) Новость 4
5) Новость 5        
            '''
        bot.send_message(message.chat.id, msg , reply_markup=mp.off_markup, parse_mode='MARKDOWN')

    except Exception as e:
        bot.reply_to(message, f'{e}')

if __name__ == "__main__":
    bot.polling(none_stop=True)






