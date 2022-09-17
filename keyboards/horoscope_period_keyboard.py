from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

import keyboards.back_to_menu_keyboard

TODAY_PERIOD_BUTTON_TEXT = 'На сегодня'
TOMORROW_PERIOD_BUTTON_TEXT = 'На завтра'

keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=TODAY_PERIOD_BUTTON_TEXT), KeyboardButton(text=TOMORROW_PERIOD_BUTTON_TEXT)],
    [KeyboardButton(text=keyboards.back_to_menu_keyboard.BACK_TO_MENU_BUTTON_TEXT)]
], resize_keyboard=True)
