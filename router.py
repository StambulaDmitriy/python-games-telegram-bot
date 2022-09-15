from aiogram.filters import Command

from bootstrap import MyDispatcher

import handlers


def register_commands():
    dp = MyDispatcher().getInstance()

    dp.message.register(handlers.start_command.start, Command(commands='start'), state=None)
