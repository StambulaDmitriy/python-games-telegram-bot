from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

HIT_BUTTON_TEXT = 'Взять ещё'
STAND_BUTTON_TEXT = 'Остановиться'

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=HIT_BUTTON_TEXT), KeyboardButton(text=STAND_BUTTON_TEXT)]
    ],
    resize_keyboard=True
)
