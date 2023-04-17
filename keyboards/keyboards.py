from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from lexicon.lexicon import CALLBACK, WARDS, MARKBOOKS


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

def show_reports(reports):
    keyboard = InlineKeyboardBuilder()

    buttons = [InlineKeyboardButton(text=f'{report[0]}\nЗарплата: {report[1]}', url=report[2]) for report in reports]

    keyboard.row(*buttons, width=3)
    
    return keyboard.as_markup()

def add_markbooks_kb():
    keyboard = InlineKeyboardBuilder()
    button = InlineKeyboardButton(text='Добавить в закладки', callback_data=MARKBOOKS['add'])
    keyboard.row(button)
    return keyboard.as_markup()

def remove_from_markbooks_kb():
    keyboard = InlineKeyboardBuilder()
    button = InlineKeyboardButton(text='Удалить из закладок', callback_data=MARKBOOKS['remove'])
    keyboard.row(button)
    return keyboard.as_markup()

def show_markbooks(marks):
    keyboard = InlineKeyboardBuilder()
    buttons = [InlineKeyboardButton(text=f'{mark[0]}', url=f'{mark[1]}') for mark in marks]

    keyboard.row(*buttons, width=1)
    return keyboard.as_markup()