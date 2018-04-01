import logging.config

import telebot
from telebot import types

import requests

TOKEN = '527154741:AAGmLFVC1xy28H6RrgMw3mbApGg8NhBZsa4'
bot = telebot.TeleBot(TOKEN)

# ================ LOGGER CONFIGURATION =================

logging.config.fileConfig(fname='log.conf')

log = logging.getLogger('main')

# =============== CONSTANTS ====================

HELP_INFO = 'Hello! I am in.Place bot\n\n' \
            'I can help you to pick up a place you want to go right now, ' \
            'just answer a few my pictured questions ;)\n\n' \
            'Use this commands:\n' \
            '/start - start bot and list all available commands\n' \
            '/help - list all available commands\n' \
            '/go - start Q/A-session\n' \
            '/echo - just echo your message'
'/joke - you can try to ask me for a joke, heh :)'

BASIC_URL = 'https://inplace-api.herokuapp.com/api/'
IMAGE_URL = 'https://inplace-api.herokuapp.com/api/images/'
PLACE_URL = 'https://inplace-api.herokuapp.com/api/places/'

ALL_PICS_URL = 'https://inplace-api.herokuapp.com/api/images/set/'
ALL_PLACES_URL = 'https://inplace-api.herokuapp.com/api/places/set/'

XKCD_MAX_COMICS_NUMBER = 1833

# ================== STATUS ====================

# True, если пользователь в стадии ответа на вопросы

STATUS = False


# ================== COMMANDS ==================
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(chat_id=message.chat.id, text=HELP_INFO)
    log.info('bot started in chat_id={}'.format(message.chat.id))


@bot.message_handler(commands=["echo"])
def echo(message):
    bot.send_message(chat_id=message.chat.id,
                     text=message.text)
    log.debug('/echo in chat_id={}'.format(message.chat.id))


@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(chat_id=message.chat.id, text=HELP_INFO)
    log.debug('/help called in chat_id={}'.format(message.chat.id))


@bot.message_handler(commands=["go"])
def session(message):
    # получить все картинки
    # TODO: какие группы картинок?
    r = requests.get(url=ALL_PICS_URL)
    pics = r.json()

    # получить все места/мероприятия
    r = requests.get(url=ALL_PLACES_URL)
    places = r.json()

    print('Number of pictures for questions: ', len(pics))
    bot.send_message(chat_id=message.chat.id,
                     text="Всего картинок для вопросов: {}".format(len(pics)))

    print('Number of places for questions: ', len(places))
    bot.send_message(chat_id=message.chat.id,
                     text="Всего мест для посещения: {}".format(len(places)))

    # настраиваем клавиатуру
    # TODO: вынести в отдельную функцию
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('1')
    itembtn2 = types.KeyboardButton('2')
    itembtn3 = types.KeyboardButton('3')
    itembtn4 = types.KeyboardButton('4')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
    bot.send_message(chat_id=message.chat.id,
                     text="Выберите одно число:",
                     reply_markup=markup)

    # помечаем, что теперь пользователь подбирает себе место
    # TODO: сколько вопросов задавать?
    global STATUS
    STATUS = True


@bot.message_handler(content_types=["text"])
def check_answer(message):
    global STATUS
    if STATUS == True:
        STATUS = False
        markup = types.ReplyKeyboardRemove(selective=False)
        bot.send_message(chat_id=message.chat.id,
                         text='Ваш ответ: {}'.format(message.text),
                         reply_markup=markup)
        log.debug('/check_answer called in chat_id={}'.format(message.chat.id))


bot.polling()
