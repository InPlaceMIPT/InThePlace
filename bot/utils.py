from telebot import types


def markup_4_buttons():
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('1')
    itembtn2 = types.KeyboardButton('2')
    itembtn3 = types.KeyboardButton('3')
    itembtn4 = types.KeyboardButton('4')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
    return markup

def markup_with_who_buttons():
    markup = types.ReplyKeyboardMarkup(row_width=1)
    itembtn1 = types.KeyboardButton('Один')
    itembtn2 = types.KeyboardButton('Со второй половинкой')
    itembtn3 = types.KeyboardButton('С семьей')
    itembtn4 = types.KeyboardButton('С друзьями')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
    return markup


def markup_money_buttons():
    markup = types.ReplyKeyboardMarkup(row_width=1)
    itembtn1 = types.KeyboardButton('менее  500 руб.')
    itembtn2 = types.KeyboardButton('от 500 руб. до 1500 руб.')
    itembtn3 = types.KeyboardButton('более 1500 руб.')
    markup.add(itembtn1, itembtn2, itembtn3)
    return markup