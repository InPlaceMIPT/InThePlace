import logging.config

import requests
import telebot
from telebot import types

import config
import utils
from token_info import TOKEN

bot = telebot.TeleBot(token=TOKEN)

# ================ LOGGER CONFIGURATION =================

logging.config.fileConfig(fname='log.conf')

log = logging.getLogger('main')

# ================== STATUS ====================

# True, если пользователь в стадии ответа на вопросы

STATUS = False


# ================== COMMANDS ==================
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(chat_id=message.chat.id, text=config.HELP_INFO)
    log.info('bot started in chat_id={}'.format(message.chat.id))


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
