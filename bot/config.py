# =============== CONSTANTS ====================

HELP_INFO = 'Привет! Я In.place бот :)\n\n' \
            'Я помогу тебе подобрать места по настроению\n' \
            'Для этого я должен узнать о тебе побольше ;)\n\n' \
            'Используй эти команды:\n' \
            '/start - запуск бота\n' \
            '/help - список возможных команд\n' \
            '/go - старт сессии вопрос/ответ\n'

START_GO_MSG = 'Для начала я бы хотел узнать твои общие требования к мероприятию :)'

COMPANY_MSG = 'С кем ты хочешь пойти на событие?'
MONEY_MSG = 'На какую сумму ты рассчитываешь?'

START_IMAGE_QUESTIONS = 'Теперь выбирай картинку по душе :)'
START_RECOMENDATION_MSG = 'Ок! Я выбираю подходящее место...'

BASIC_URL = 'https://inplace-api.herokuapp.com/api/'
IMAGE_URL = 'https://inplace-api.herokuapp.com/api/images/'
PLACE_URL = 'https://inplace-api.herokuapp.com/api/places/'
RECOMMEND_URL = 'https://inplace-api.herokuapp.com/api/recommend/byimageid/'
INFO_LIST_URL = 'https://inplace-api.herokuapp.com/api/places/info/list/'

FOUR_PICS_URL = 'https://inplace-api.herokuapp.com/api/images/4set/url/'
FOUR_PICS_IDS = 'https://inplace-api.herokuapp.com/api/images/4set/ids/'
ALL_PICS_URL = 'https://inplace-api.herokuapp.com/api/images/set/'
ALL_PLACES_URL = 'https://inplace-api.herokuapp.com/api/places/set/'

N_GROUPS = 4


def gen_place_output(place):
    responce_msg = 'Название: {}\nВремя: {}\nАдрес: Долгопрудный, {}\nОписание: {}\n'.format(
        place['title'], place['timetable'], place['address'], place['description']
    )
    return responce_msg
