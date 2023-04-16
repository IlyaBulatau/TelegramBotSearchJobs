from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from lexicon.lexicon import CALLBACK, WARDS


def choice_sort_kb():
    keyboard = InlineKeyboardBuilder()

    buttons = [
        InlineKeyboardButton(text='По зарплате(по убыванию)', callback_data=CALLBACK['salary']),
        InlineKeyboardButton(text='По дате(сначала новые)', callback_data=CALLBACK['date'])
    ]

    keyboard.row(*buttons)
    return keyboard.as_markup()

def show_requests(requests, len_requests, current_page):

    keyboard = InlineKeyboardBuilder()
    buttons = [InlineKeyboardButton(text=request[0], callback_data=request[0]) for request in requests]

    wards = [InlineKeyboardButton(text=v, callback_data=k) for k, v in WARDS.items()]
    forward, backward = wards

    count_page = InlineKeyboardButton(text=f'{current_page}/{len_requests}', callback_data='current_page')

    keyboard.row(*buttons, width=1)
    keyboard.row(forward, count_page, backward)
    
    return keyboard.as_markup()

