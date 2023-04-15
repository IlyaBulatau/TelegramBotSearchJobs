from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from lexicon.lexicon import CALLBACK

def choice_sort_kb():
    keyboard = InlineKeyboardBuilder()
    buttons = [
        InlineKeyboardButton(text='По зарплате(по убыванию)', callback_data=CALLBACK['date']),
        InlineKeyboardButton(text='По дате(сначала новые)', callback_data=CALLBACK['salary'])
    ]

    keyboard.row(*buttons)
    return keyboard.as_markup()
