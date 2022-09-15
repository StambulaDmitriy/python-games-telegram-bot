from aiogram.types import BotCommand

from bootstrap import MyBot


async def register_default_commands():
    bot = MyBot().getInstance()
    return await bot.set_my_commands(
        commands=[
            BotCommand(command='start', description='Начать работу с ботом'),
            BotCommand(command='help', description='Узнать правила'),
            BotCommand(command='balance', description='Узнать текущий баланс')
        ]
    )
