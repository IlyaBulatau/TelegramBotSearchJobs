from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from lexicon.lexicon import CALLBACK, WARDS, MARKBOOKS


def choice_sort_kb():
    """
    Клавиатура для выбора критерия при поиске вакансий
    """
    keyboard = InlineKeyboardBuilder()

    buttons = [
        InlineKeyboardButton(text='По зарплате(по убыванию)', callback_data=CALLBACK['salary']),
        InlineKeyboardButton(text='По дате(сначала новые)', callback_data=CALLBACK['date'])
    ]

    keyboard.row(*buttons)
    return keyboard.as_markup()

def show_requests(requests, len_requests, current_page):
    """
    Клавиатура отображения номера страницы списка запросов
    """
    keyboard = InlineKeyboardBuilder()
    buttons = [InlineKeyboardButton(text=request[0], callback_data=request[0]) for request in requests]

    wards = [InlineKeyboardButton(text=v, callback_data=k) for k, v in WARDS.items()]
    forward, backward = wards

    count_page = InlineKeyboardButton(text=f'{current_page}/{len_requests}', callback_data='current_page')

    keyboard.row(*buttons, width=1)
    keyboard.row(forward, count_page, backward)
    
    return keyboard.as_markup()

def show_reports(reports):
    """
    Клавиатура отображения результатов поиска по запросу
    """
    keyboard = InlineKeyboardBuilder()

    buttons = [InlineKeyboardButton(text=f'{report[0]}\nЗарплата: {report[1]}', url=report[2]) for report in reports]

    keyboard.row(*buttons, width=3)
    
    return keyboard.as_markup()

def add_markbooks_kb():
    """
    Клавиатура для надписи добавить в закладки под вакансией
    """
    keyboard = InlineKeyboardBuilder()
    button = InlineKeyboardButton(text='Добавить в закладки', callback_data=MARKBOOKS['add'])
    keyboard.row(button)
    return keyboard.as_markup()

def remove_from_markbooks_kb():
    """
    Клавиатура для надписи под вакансияй для удаления из закладок
    """
    keyboard = InlineKeyboardBuilder()
    button = InlineKeyboardButton(text='Удалить из закладок', callback_data=MARKBOOKS['remove'])
    keyboard.row(button)
    return keyboard.as_markup()

def show_markbooks(marks):
    """
    Клавиатура отображает Закладки
    """
    keyboard = InlineKeyboardBuilder()
    edit_button = InlineKeyboardButton(text='✅ Редактировать', callback_data='edit_marksbook')
    buttons = [InlineKeyboardButton(text=f'⭐ {mark[0]}', url=mark[1], callback_data=f'{mark[1]}') for mark in marks]

    keyboard.row(*buttons, width=1)
    keyboard.row(edit_button)
    return keyboard.as_markup()

def edit_marksbook(marks):
    """
    Клавиатура отображает удаление из закладок
    """
    keyboard = InlineKeyboardBuilder()
    
    buttons_marks = [InlineKeyboardButton(text=f'❌ {mark[0]}',callback_data=f'del_{mark[1]}') for mark in marks]
    button_cancel = InlineKeyboardButton(text='Назад', callback_data=MARKBOOKS['Назад'])

    keyboard.row(*buttons_marks, width=1)
    keyboard.row(button_cancel)

    return keyboard.as_markup()