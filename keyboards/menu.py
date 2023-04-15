from aiogram.types.bot_command import BotCommand

from lexicon.lexicon import COMMANDS

async def menu(bot):

    commands = [
        BotCommand(
        command=COMMANDS['start'],
        description='Старт'
        ),
        BotCommand(
        command=COMMANDS['job'],
        description='Поиск работы'
        ),
        (
        BotCommand(
        command=COMMANDS['cancel'],
        description='Закончить'
        )
        )
    ]

    await bot.set_my_commands(commands)