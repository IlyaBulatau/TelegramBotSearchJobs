"""
Модуль парсит данные вакансий по запросу пользователя:
Название проффесии
Сортировка - дата(date), зарплата(salary)
Парсит первые (15, 30, 45) вакансий
"""

import asyncio
import re
from pyppeteer import launch

from database import orm, models

async def get_jobs(browser, prfs, page, sort, datetime_now, user_id) -> str:
    """
    Открывает страницу по запросу професся, критерий, кол-во страниц
    вызывает функцию get_data_job для парсинга страницы

    browser:: Обьект браузера
    prfc:: Запрос вакансии
    count_page:: Запрос количества результатов
    sort:: Запрос критерия сортировки
    datetime_now:: Время для записи request_id в базу данных, пример - 2023_Apr_17_20h_28m_26s
    user_id:: ID юзера для записи в базу данных
    """
    page = await browser.newPage()
    # await page.setViewport({'width': 1900, 'height': 1000})
    await page.goto(url=f'https://belmeta.com/vacansii?q={prfs}&l=Минск&sort={sort}&page={page}')
    data= []
    jobs = await page.querySelectorAll('.title-wrap')
    for job in jobs:
        job = await job.querySelector('a')
        link = 'https://belmeta.com'+await page.evaluate('(element) => element.getAttribute("href")', job)
        data.append(link)

    tasks = []
    for link in data:
        task = asyncio.create_task(get_data_job(browser, link, datetime_now, user_id))
        tasks.append(task)
    
    await asyncio.gather(*tasks)
    await page.close()
    

async def get_data_job(browser, url, datetime_now, user_id):
    """
    Получает ссылку на вакансию, парсит со страницы все данные и сохраняет в базу данных

    browser:: Экзепляр браузера
    url:: Ссылка на вакансию
    datetime_now:: Время для записи request_id в базу данных, пример - 2023_Apr_17_20h_28m_26s
    user_id:: ID юзера для записи в базу данных
    """
    page = await browser.newPage()
    # await page.setViewport({'width': 1900, 'height': 1000})
    await page.goto(url)

    title_tag = await page.waitForSelector('h1')
    title = await page.evaluate('(element) => element.textContent', title_tag)

    try:
        salare_tag = await page.waitForSelector('.value')
        salary = await page.evaluate('(element) => element.textContent', salare_tag)
        compile = re.compile('.*\d+.*')
        salary = re.findall(compile, salary)[0]
    except:
        salary = 'Не указана'

    try:
        descriptions_tag = await page.waitForSelector('body > div.container-fluid > div > main > div > div > div:nth-child(10)', timeout=5000)
        descriptions = await page.evaluate('(element) => element.textContent', descriptions_tag)
    except:
        descriptions = '-'
    


    data = {'title': title, 'salary': salary, 'description': descriptions[:999], 'link': url}

    orm.write_report_in_db(data, models.Report, user_id, datetime_now)

    await page.close()
    

async def get_info(prfs: str, count_page: int, sort: str, datetime_now: str, user_id: int) -> None:
    """
    Открывает браузер, создает таски, выполняет таски, закрывает браузер

    prfc:: Запрос вакансии
    count_page:: Запрос количества результатов
    sort:: Запрос критерия сортировки
    datetime_now:: Время для записи request_id в базу данных, пример - 2023_Apr_17_20h_28m_26s
    user_id:: ID юзера для записи в базу данных
    """
    if count_page < 16:
        count_page = 1
    elif 15 < count_page < 31:
        count_page = 2
    else:
        count_page = 3 
    browser = await launch()
    tasks = []
    for page in range(1, count_page+1):
        task = asyncio.create_task(get_jobs(browser, prfs, page, sort, datetime_now, user_id))
        tasks.append(task)
    
    await asyncio.gather(*tasks)
    await browser.close()


