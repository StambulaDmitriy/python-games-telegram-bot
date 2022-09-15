from aiogram import F
from aiogram.filters import Command

import keyboards.main_menu_keyboard
from bootstrap import MyDispatcher

import handlers
from keyboards.inline import HelpCallbackData


def register_commands():
    dp = MyDispatcher().getInstance()

    dp.message.register(handlers.start, Command(commands='start'), state=None)

    dp.message.register(handlers.help_command, Command(commands='help'))
    dp.message.register(handlers.help_command, F.text == keyboards.main_menu_keyboard.RULES_BUTTON_TEXT, state=None)
    dp.callback_query.register(handlers.help_inline_callback, HelpCallbackData.filter())

    dp.message.register(handlers.balance_command, F.text == keyboards.main_menu_keyboard.BALANCE_BUTTON_TEXT, state=None)
    dp.message.register(handlers.balance_command, Command(commands='balance'), state=None)

