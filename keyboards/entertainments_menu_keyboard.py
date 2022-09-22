from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

import keyboards

MAGIC_8_BALL_BUTTON_TEXT = '🎱 Шар предсказаний'
HOROSCOPE_BUTTON_TEXT = '🪬 Гороскоп'
JOKE_BUTTON_TEXT = '😂 Анекдот'

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=MAGIC_8_BALL_BUTTON_TEXT)],
        [KeyboardButton(text=HOROSCOPE_BUTTON_TEXT)],
        [KeyboardButton(text=JOKE_BUTTON_TEXT)],
        [KeyboardButton(text=keyboards.back_to_menu_keyboard.BACK_TO_MAINMENU_BUTTON_TEXT)]
    ],
    resize_keyboard=True
)


async def send_keyboard(message: types.Message):
    await message.answer("Выберите пункт меню:", reply_markup=keyboard)
