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

async def get_jobs(browser, prfs, page, sort, datetime_now):
    """
    Получает страницу по запросу профессии, парсит ссылки на все вакансии,
    с помощью функции
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
        task = asyncio.create_task(get_data_job(browser, link, datetime_now))
        tasks.append(task)
    
    await asyncio.gather(*tasks)
    await page.close()
    

async def get_data_job(browser, url, datetime_now):
    """
    Получает ссылку на вакансию, парсит со страницы все данные и сохраняет в базу данных
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

    orm.write_report_in_db(data, models.Report, datetime_now)

    await page.close()
    

async def get_info(prfs, count_page, sort, datetime_now):
    """
    Открывает браузер, создает таски, выполняет таски, закрывает браузер
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
        task = asyncio.create_task(get_jobs(browser, prfs, page, sort, datetime_now))
        tasks.append(task)
    
    await asyncio.gather(*tasks)
    await browser.close()

#ПРИМЕР ЗАПУСКА
# asyncio.run(get_info('Python', 1, 'date'))





