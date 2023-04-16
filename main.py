from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, Redis

import asyncio

from handlers.handlers import router
from config import load_token
from keyboards import menu

async def run_bot():
    redis = Redis(host='localhost')
    storage = RedisStorage(redis=redis)

    bot = Bot(token=load_token())
    dp = Dispatcher(storage=storage)

    dp.include_router(router)
    dp.startup.register(menu.menu)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(run_bot())

# TODO - Сделать возможность просматривать предидущие запросы, а так же добавлять вакансии в закладки
# добавить кнопку под ответам с вакансия "Добавить в зкладки" при добавлении сменить кнопку на "В закладке"
# Добавить команду /reports - просмотр предидущих запросов при клике на запрос поевляется инлайн-клавиатура с вакансиями запроса и пагинацияй 