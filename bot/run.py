import logging.config

import requests
import telebot

import config
import utils
from token_info import TOKEN

bot = telebot.TeleBot(token=TOKEN)

# ================ LOGGER CONFIGURATION =================

logging.config.fileConfig(fname='log.conf')

log = logging.getLogger('main')

# ================== STATUS ====================

# True, если пользователь в стадии ответа на вопросы

users_info = {}


# ================== COMMANDS ==================
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(chat_id=message.chat.id, text=config.HELP_INFO)
    log.info('bot started in chat_id={}'.format(message.chat.id))
    users_info[message.chat.id] = [False, 0, []]


@bot.message_handler(commands=["echo"])
def echo(message):
    bot.send_message(chat_id=message.chat.id,
                     text=message.text)
    log.debug('/echo in chat_id={}'.format(message.chat.id))


@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(chat_id=message.chat.id, text=config.HELP_INFO)
    log.debug('/help called in chat_id={}'.format(message.chat.id))


@bot.message_handler(commands=["go"])
def session(message):
    # получить все картинки
    # TODO: какие группы картинок?
    r = requests.get(url=config.ALL_PICS_URL)
    pics = r.json()
    print(pics)

    # получить все места/мероприятия
    r = requests.get(url=config.ALL_PLACES_URL)
    places = r.json()

    print('Number of pictures for questions: ', len(pics))
    bot.send_message(chat_id=message.chat.id,
                     text="Всего картинок для вопросов: {}".format(len(pics)))

    print('Number of places for questions: ', len(places))
    bot.send_message(chat_id=message.chat.id,
                     text="Всего мест для посещения: {}".format(len(places)))

    # настраиваем клавиатуру
    markup = utils.markup_4_buttons()
    bot.send_message(chat_id=message.chat.id,
                     text="Выберите одно число:",
                     reply_markup=markup)

    users_info[message.chat.id][0] = True
    send_image(message, users_info[message.chat.id][1])


@bot.message_handler(content_types=['text'])
def check_answer(message):
    if message.text in ['1', '2', '3', '4'] and users_info[message.chat.id][0]:
        users_info[message.chat.id][2].append(message.text)
        users_info[message.chat.id][1] += 1
        if users_info[message.chat.id][1] < config.N_GROUPS:
            send_image(message, users_info[message.chat.id][1])
        else:
            recommend_event(message)


def recommend_event(message):
    bot.send_message(chat_id=message.chat.id, text='ок! Я выбираю подходящее место...')
    r = requests.post(url=config.RECOMEND_URL, json={'images': [224, 430]})
    events = r.json()
    for event in events:
        pass


def send_image(message, n_group):
    print('!!!', n_group)
    r = requests.get(url=config.FOUR_PICS_IDS, params={'group': '{}'.format(n_group)})
    print(r.json())
    r = requests.get(url=config.FOUR_PICS_URL, params={'group': '{}'.format(n_group)})
    print('!!!!!!!!!!')
    print(r.json())
    image_link = r.json()['image']
    bot.send_photo(chat_id=message.chat.id, photo=image_link)


bot.polling()
