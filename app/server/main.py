import os
import telebot
from telebot import types
import markup as mp
from dotenv import load_dotenv
from telegram_bot_pagination import InlineKeyboardPaginator

import sys

sys.path.insert(1, os.path.join(sys.path[0], '../'))
from database.dbworker import get_post


from Levenshtein import distance as lev_distance
from collections import Counter, defaultdict
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
from tqdm import tqdm
import random
import heapq
import re

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
sns.set(context='notebook', style='whitegrid', palette='pastel',
        font='sans-serif', font_scale=1, color_codes=False, rc=None)

from nltk import pos_tag, WordNetLemmatizer
from nltk.corpus import stopwords, wordnet
from nltk.tokenize import word_tokenize
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('all')

import warnings
warnings.filterwarnings("ignore")


data = pd.read_csv('csv/data.csv')

def clear(string: str):
    punkt_list = ['.', ',', '/', '`', '"', "'", '!', '&', '?', '(', ')', '-', '+', '_', '*', '@', ';', ':', '<',
             '>', '\\', '[', ']', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '“', '„', '%', '$', '…',
             '’', '|', '^', '~', '=', '»', '”', '′', '•', '—', '«', '–', '№']

    stop_list = stopwords.words('russian') + stopwords.words('english')
    rubbish_list = ['которые', 'нам', 'дали', 'например', 'пока', 'часть', 'лишь', 'это', 'также', 'будут',
                    'россии', 'россия', 'года', 'годы', 'году', 'год', 'январь', 'января', 'февраля', 'могут',
                    'февраль', 'март', 'марта', 'апрель', 'апреля', 'май', 'мая', 'июнь', 'июня', 'июль',
                    'июля', 'август', 'августа', 'сентябрь', 'сентября', 'октябрь', 'октября', 'ноябрь',
                    'ноября', 'декабрь', 'декабря', 'москва', 'interfaxru', 'сша', 'рф', 'млн', 'млрд', 'тыс',
                    'рубль', 'рублей', 'рубля', 'рублю', 'сентябре', 'январе', 'феврале', 'марте', 'апреле',
                    'мае', 'июне', 'июле', 'августе', 'октябре', 'ноябре', 'декабре', 'говорится', 'ранее',
                    'изза', 'когдалибо', 'когдато', 'гделибо', 'гдето', 'московской', 'сообщил', 'составил',
                    'новых', 'новые', 'понедельник', 'вторник', 'среду', 'четверг', 'пятницу', 'субботу',
                    'воскресенье', 'рост', 'роста', 'фоне', 'итогам', 'итоги', 'время', 'стран', 'страна',
                    'который', 'словам', 'начала', 'сранению', 'заявил', 'руб', 'числе', 'сообщила', 'решение',
                    'страны', 'тысяч', 'конце', 'около', 'сказал', 'российских', 'однако', 'данным', 'дня',
                    'сообщении', 'относительно', 'возможность', 'пишет', 'времени', 'период', 'которых',
                    'неделе', 'российской', 'рамках', 'отмечает', 'поскольку', 'месяцев', 'отметил', 'ходе',
                    'срок', 'тонн', 'является', 'сообщает', 'российского', 'которая', 'составила', 'открылся',
                    'российские', 'количество', 'впервые']
    stop_list += rubbish_list
    for sign in punkt_list:
        string = string.replace(sign, '') # чистка знаков препинания
    string = string.replace('\n', ' ') # чистка переносов строки
    string = string.replace('\t', ' ') # чистка табов
    string = string.replace('  ', ' ') # удаление двойных пробелов
    string = word_tokenize(string) # токенизация по словам
    string = [word for word in string if not word in stop_list] # удаление стоп-слов
    return string

def clear_data(data):
    data = data.dropna()
    data = data.reset_index(drop=True)
    for i in range(data.shape[0]):
        data.loc[i, 'text'] = data.loc[i, 'text'].lower()
    for i in tqdm(range(data.shape[0])):
        string = data.loc[i, 'text']
        string = clear(string)
        data.loc[i, 'text'] = ''
        for j in string:
            data.loc[i, 'text'] += ' '+j
        data.loc[i, 'text'] = data.loc[i, 'text'][1:]
    return data

def delenie(data):
    text_list = []
    for i in tqdm(range(len(data))):
        text_list.append(data.loc[i, 'text'])
    return text_list

def Vectorization(corpus):
    X = TfidfVectorizer().fit_transform(corpus).toarray()
    return X

def train(data):
    X = Vectorization(delenie(clear_data(data)))
    kmeans = KMeans(n_clusters = 10, init = "k-means++", max_iter = 50, n_init = 100, random_state = 1)
    kmeans.fit(X)
    return X, kmeans.predict(X), kmeans

X, y, kmeans = train(data)

def Mapping(kmeans):
    label = kmeans.labels_
    map = {}
    for l in tqdm(range(len(label))):
        if  label[l] not in map:
            map[label[l]] = [l]
        else:
            map[label[l]].append(l)
    return map

Map = Mapping(kmeans)

def getReccomendation(cat, data, X, y, Map):
    index = random.choice(Map[cat])
    prediction = y[index]
    vector_arr = []
    id_arr = []
    for i in Map[prediction]:
        if i != index:
            vector_arr.append(X[i])
            id_arr.append(i)
    vector_arr = np.array(vector_arr)
    sim_array = list(cosine_similarity([X[index]], vector_arr)[0])
    K = 8
    gen_rec = []
    for i in range(len(id_arr)):
        gen_rec.append((id_arr[i], sim_array[i]))
    gen_rec = sorted(gen_rec, key=lambda x: x[1], reverse=True)[:K]
    return [data.loc[ind[0], 'href'] for ind in gen_rec]


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

@bot.message_handler(commands=['news'])
def news(message) -> None:
    try:
        unique_code = extract_unique_code(message.text)
        output = getReccomendation(int(unique_code),data,X,y,Map)
        msg = ''
        for i in range(len(output)):
            post = get_post(href=output[i])
            msg += f'[{post.title}]({output[i]}\n'

        bot.send_message(message.chat.id, msg, reply_markup=mp.like_dislike, parse_mode='MARKDOWN')

    except Exception as e:
        bot.reply_to(message, f'{e}')

def extract_unique_code(text):
    return text.split()[1] if len(text.split()) > 1 else None


# @server.callback_query_handler(func=lambda call: call.data.split('#')[0] == 'character')
# def page_callback(call):
#     page = int(call.data.split('#')[1])
#     server.delete_message(
#         call.message.chat.id,
#         call.message.message_id
#     )
#     send_posts_page(call.message, page)
#
#
# def send_posts_page(message, page=1):
#     data_pages = data_page()
#     paginator = InlineKeyboardPaginator(
#         len(data_pages),
#         current_page=page,
#         data_pattern='character#{page}'
#     )
#
#     server.send_message(
#         message.chat.id,
#         data_pages[page - 1],
#         reply_markup=paginator.markup,
#         parse_mode='Markdown'
#     )
#
#
# def data_page():
#     output =
#
#     data_pages = []
#     i = 0
#     sample = ' '
#     for j in range(len(output)):
#         i += 1
#         sample = sample + f' ``` {output[j]} ``` \n'
#         if i % 20 == 0:
#             data_pages.append(sample)
#             sample = ' '
#
#     return data_pages


print(1)
bot.polling(none_stop=True)






