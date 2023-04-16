from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from lexicon.lexicon import CALLBACK, WARDS
from services.converting import converting_datetime


def choice_sort_kb():
    keyboard = InlineKeyboardBuilder()

    buttons = [
        InlineKeyboardButton(text='По зарплате(по убыванию)', callback_data=CALLBACK['date']),
        InlineKeyboardButton(text='По дате(сначала новые)', callback_data=CALLBACK['salary'])
    ]

    keyboard.row(*buttons)
    return keyboard.as_markup()

def show_requests(requests, len_requests):

    keyboard = InlineKeyboardBuilder()
    buttons = [InlineKeyboardButton(text=converting_datetime(request[0]), callback_data=converting_datetime(request[0])) for request in requests]

    wards = [InlineKeyboardButton(text=v, callback_data=k) for k, v in WARDS.items()]
    forward, backward = wards

    count_page = InlineKeyboardButton(text=f'current/{len_requests}', callback_data='current_page')

    keyboard.row(*buttons, width=1)
    keyboard.row(forward, count_page, backward)
    
    return keyboard.as_markup()

