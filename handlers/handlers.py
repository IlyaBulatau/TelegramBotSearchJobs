from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext

import datetime
import math

from handlers.fsm import JobsForm
from lexicon.lexicon import COMMANDS, CALLBACK, WARDS
from keyboards import keyboards
from handlers.filters import is_valid_count, is_valid_job, is_requests_callback
from services import services, converting
from database import orm
from database.models import User, Request, Report, Page

router = Router()

@router.message(Command(commands=COMMANDS['start']))
async def command_start(message: Message):
    if orm.is_user_in_db(message.from_user.id, User):
        orm.add_user_to_db(message.from_user.id, User, Page)
    await message.answer(text=f'Привет {message.from_user.first_name}, я предоставляю информацию о вакансиях\n\nДля взаимодействия со мной используй меню')

@router.message(Command(commands=COMMANDS['cancel']))
async def command_cancel(message: Message, state: FSMContext):
    status_state = await state.get_state()
    if status_state == None:
        return
    await state.clear()
    await message.answer('Поиск вакансий прекращен')

@router.message(Command(commands=COMMANDS['show']))
async def command_show(message: Message):
    requests = orm.get_request_in_db(message.from_user.id, Request)
    len_requests = math.ceil(len(requests) / 5) 
    if requests == []:
        await message.answer(text='Вы пока не искали работу\n\nДля поиска работы введите /job')
    else:
        orm.update_current_page(message.from_user.id, Page, 1)
        current_page = orm.get_current_page_in_db(message.from_user.id, Page)
        requests = requests[current_page*5-5:current_page*5]
        await message.answer(text='Ваша история поиска по дате', reply_markup=keyboards.show_requests(requests, len_requests, current_page))

@router.message(Command(commands=COMMANDS['job']))
async def command_job(message: Message, state: FSMContext):
    await state.set_state(JobsForm.job)
    await message.answer(text='Вы начали поиск вакансии, введите профессию\n\nЕсли хотите закончить поиск выберите команду /cancel')

@router.message(JobsForm.job, is_valid_job)
async def process_job_add(message: Message, state: FSMContext):
    await state.update_data(job=message.text)
    await state.set_state(JobsForm.sort)
    await message.answer(text='Выберите по какому критерию сортировать результат поиска', reply_markup=keyboards.choice_sort_kb())

@router.message(JobsForm.job)
async def process_job_not(message: Message):
    await message.answer(text='Пожалуйста, введите существующую проффессию')

@router.callback_query(JobsForm.sort, Text(text=[CALLBACK['date'], CALLBACK['salary']]))
async def process_sort_add(callback: CallbackQuery, state: FSMContext):
    await state.update_data(sort=callback.data)
    await state.set_state(JobsForm.count)
    await callback.message.answer(text='Введите количество результатов которые хотите получить\nмаксимум - 45')

@router.message(JobsForm.sort)
async def process_sort_not(message: Message):
    await message.answer(text='Пожайлуйста, выберите критерий сортировки', reply_markup=keyboards.choice_sort_kb())

@router.message(JobsForm.count, is_valid_count)
async def process_count_add(message: Message, state: FSMContext):
    await state.update_data(count=message.text)
    data = await state.get_data()
    count = int(data['count'])

    datetime_now = converting.converting_datetime(datetime.datetime.now())
    orm.write_request_in_db(data, Request, message.from_user.id, datetime_now)
    await services.get_info(data['job'], int(data['count']), data['sort'], datetime_now)
    await state.clear()

    answers = orm.get_current_report_in_db(datetime_now, Report, count)
    for answer in answers:
        await message.answer(text=f"""{answer[0]}
        Зарплата: {answer[1]}
        Ссылка: {answer[2]}
        """)

@router.message(JobsForm.count)
async def process_count_not(message: Message):
    await message.answer(text='Пожалуйста, введите целое число от 1 до 45')

@router.callback_query(Text(text='forward'))
async def process_forward_page(callback: CallbackQuery):
    current_page = orm.get_current_page_in_db(callback.from_user.id, Page)
    requests = orm.get_request_in_db(callback.from_user.id, Request)
    len_requests = math.ceil(len(requests) / 5)
    if current_page < len_requests:
        current_page += 1
        orm.update_current_page(callback.from_user.id, Page, current_page)
        requests = requests[current_page*5-5:current_page*5]
        await callback.message.edit_text(text='Ваша история поиска по дате', reply_markup=keyboards.show_requests(requests, len_requests, current_page))


@router.callback_query(Text(text='backward'))
async def process_backward_page(callback: CallbackQuery):
    current_page = orm.get_current_page_in_db(callback.from_user.id, Page)
    requests = orm.get_request_in_db(callback.from_user.id, Request)
    len_requests = math.ceil(len(requests) / 5)
    if current_page > 1:
        current_page -= 1
        orm.update_current_page(callback.from_user.id, Page, current_page)
        requests = requests[current_page*5-5:current_page*5]
        await callback.message.edit_text(text='Ваша история поиска по дате', reply_markup=keyboards.show_requests(requests, len_requests, current_page))

@router.callback_query(is_requests_callback)
async def process_show_report(callback: CallbackQuery):
    reports = orm.get_reports_in_db(callback.data, Report)
    request_id = callback.data
    request = orm.get_request_job_in_db(callback.from_user.id, Request, request_id)[0]
    await callback.message.answer(text=f'Запрос: {request}', reply_markup=keyboards.show_reports(reports))