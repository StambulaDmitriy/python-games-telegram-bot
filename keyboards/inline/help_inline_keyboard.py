from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.inline.help_callback_data import HelpCallbackData

help_inline_keyboard_builder = InlineKeyboardBuilder()
help_inline_keyboard_builder.button(text="Кости", callback_data=HelpCallbackData(game="dice"))
help_inline_keyboard_builder.button(text="Рулетка", callback_data=HelpCallbackData(game="roulette"))
help_inline_keyboard_builder.button(text="Багелс", callback_data=HelpCallbackData(game="bagels"))
help_inline_keyboard_builder.button(text="Блекджек", callback_data=HelpCallbackData(game="blackjack"))

help_inline_keyboard = help_inline_keyboard_builder.as_markup()
