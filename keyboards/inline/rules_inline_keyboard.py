from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.inline.rules_callback_data import RulesCallbackData

rules_inline_keyboard_builder = InlineKeyboardBuilder()
rules_inline_keyboard_builder.button(text="Кости", callback_data=RulesCallbackData(game="dice"))
rules_inline_keyboard_builder.button(text="Рулетка", callback_data=RulesCallbackData(game="roulette"))
rules_inline_keyboard_builder.button(text="Багелс", callback_data=RulesCallbackData(game="bagels"))
rules_inline_keyboard_builder.button(text="Блекджек", callback_data=RulesCallbackData(game="blackjack"))

rules_inline_keyboard = rules_inline_keyboard_builder.as_markup()
