from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

BACK_TO_MENU_BUTTON_TEXT = '🔙 Назад в главное меню'

keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=BACK_TO_MENU_BUTTON_TEXT)]
], resize_keyboard=True)
