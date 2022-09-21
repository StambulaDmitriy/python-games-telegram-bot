from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

BACK_TO_MENU_BUTTON_TEXT = '🔙 Назад'
BACK_TO_MAINMENU_BUTTON_TEXT = '🔙 Назад в главное меню'

to_submenu_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=BACK_TO_MENU_BUTTON_TEXT)]
], resize_keyboard=True)

to_mainmenu_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=BACK_TO_MAINMENU_BUTTON_TEXT)]
], resize_keyboard=True)
