from telebot import types


def markup_4_buttons():
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('1')
    itembtn2 = types.KeyboardButton('2')
    itembtn3 = types.KeyboardButton('3')
    itembtn4 = types.KeyboardButton('4')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
    return markup
