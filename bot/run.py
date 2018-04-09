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
    users_info[message.chat.id] = [False, 0, [], []]


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
    markup = utils.markup_with_who_buttons()
    bot.send_message(chat_id=message.chat.id,
                     text=config.START_GO_MSG + '\n' + config.COMPANY_MSG,
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def check_answer(message):
    if message.text in ['1', '2', '3', '4'] and users_info[message.chat.id][0]:
        users_info[message.chat.id][1] += 1
        if users_info[message.chat.id][1] < config.N_GROUPS:
            users_info[message.chat.id][2].append(
                int(users_info[message.chat.id][-1][int(message.text) - 1])
            )
            send_image(message, users_info[message.chat.id][1])
            print('_____!!!!!!!!!!__________ ', users_info[message.chat.id])
            print('_user_info_', users_info[message.chat.id][2])
        else:
            recommend_event(message)
    if message.text in ['Один', 'Со второй половинкой', 'С семьей', 'С друзьями']:
        markup = utils.markup_money_buttons()
        bot.send_message(chat_id=message.chat.id, text=config.MONEY_MSG, reply_markup=markup)

    if message.text in ['менее  500 руб.', 'от 500 руб. до 1500 руб.', 'более 1500 руб.']:
        image_question(message)


def recommend_event(message):
    bot.send_message(chat_id=message.chat.id, text=config.START_RECOMENDATION_MSG)
    print('user_info in recomend_event', users_info[message.chat.id][2])
    r = requests.post(url=config.RECOMMEND_URL, json={'images': users_info[message.chat.id][2]})
    events = r.json()['events']
    print('events', events)
    r = requests.post(url=config.INFO_LIST_URL, json={'events': events})
    places = r.json()['places']
    print('places', places)
    places = places if len(places) < 4 else places[:3]
    for place in places:
        response_msg = config.gen_place_output(place)
        location = place['location']
        bot.send_message(chat_id=message.chat.id, text=response_msg)
        bot.send_location(chat_id=message.chat.id,
                          longitude=location['longitude'], latitude=location['latitude'])


def image_question(message):
    r = requests.get(url=config.ALL_PICS_URL)
    pics = r.json()
    print(pics)

    # получить все места/мероприятия
    r = requests.get(url=config.ALL_PLACES_URL)
    places = r.json()

    print('Number of pictures for questions: ', len(pics))
    print('Number of places for questions: ', len(places))

    users_info[message.chat.id][0] = True
    markup = utils.markup_4_buttons()
    bot.send_message(chat_id=message.chat.id, text=config.START_IMAGE_QUESTIONS,
                     reply_markup=markup)
    send_image(message, users_info[message.chat.id][1])


def send_image(message, n_group):
    print('!!!', n_group)
    r = requests.get(url=config.FOUR_PICS_IDS, params={'group': '{}'.format(n_group)})
    print(r.json())
    r = requests.get(url=config.FOUR_PICS_URL, params={'group': '{}'.format(n_group)})
    print('!!!!!!!!!!')
    print(r.json())
    image_link = r.json()['image']
    bot.send_photo(chat_id=message.chat.id, photo=image_link)
    users_info[message.chat.id][-1] = r.json()['images']


if __name__ == '__main__':
    bot.polling(none_stop=True)
