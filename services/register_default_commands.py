from aiogram.types import BotCommand

from bootstrap import MyBot


async def register_default_commands():
    bot = MyBot().getInstance()
    return await bot.set_my_commands(
        commands=[
            BotCommand(command='start', description='Начать работу с ботом'),
            BotCommand(command='help', description='Узнать правила'),
            BotCommand(command='support', description='Обратиться за помощью в поддержку'),
            BotCommand(command='balance', description='Узнать текущий баланс'),
            BotCommand(command='dice', description='Начать игру в кости'),
            BotCommand(command='roulette', description='Начать игру в рулетку'),
            BotCommand(command='bagels', description='Начать игру в Багелс'),
            BotCommand(command='blackjack', description='Начать игру Блекджек'),
            BotCommand(command='halyava', description='Получить денег нахаляву'),
            BotCommand(command='horoscope', description='Узнать гороскоп'),
        ]
    )
