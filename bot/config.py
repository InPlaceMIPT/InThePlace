# =============== CONSTANTS ====================

HELP_INFO = 'Привет! Я In.place бот!\n\n' \
            'Я помогу выбрать тебе __ прямо сейчас' \
            'Просто выбирай картинки по душе ;)\n\n' \
            'Используй эти команды:\n' \
            '/start - запуск бота\n' \
            '/help - споисок возможных команд\n' \
            '/go - старт сессии вопрос/ответ\n' \
            '/echo - ввод == вывод'
'/joke - а может именно тебе повезет?)'

BASIC_URL = 'https://inplace-api.herokuapp.com/api/'
IMAGE_URL = 'https://inplace-api.herokuapp.com/api/images/'
PLACE_URL = 'https://inplace-api.herokuapp.com/api/places/'
RECOMEND_URL = 'https://inplace-api.herokuapp.com/api/recommend/byimageid/'
INFO_LIST_URL = 'https://inplace-api.herokuapp.com/api/places/info/list/'

FOUR_PICS_URL = 'https://inplace-api.herokuapp.com/api/images/4set/url/'
FOUR_PICS_IDS = 'https://inplace-api.herokuapp.com/api/images/4set/ids/'
ALL_PICS_URL = 'https://inplace-api.herokuapp.com/api/images/set/'
ALL_PLACES_URL = 'https://inplace-api.herokuapp.com/api/places/set/'

N_GROUPS = 2


def gen_place_output(place):
    responce_msg = 'Название: {}\nВремя: {}\nАдрес: {}\n\nОписание: {}\n'.format(
        place['title'], place['timetable'], place['address'], place['description']
    )
    return responce_msg
