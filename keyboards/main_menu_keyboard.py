from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bootstrap import MyBot

GAMES_BUTTON_TEXT = '🎮 Игры'
ENTERTAINMENTS_BUTTON_TEXT = '🧩 Развлечения'
RULES_BUTTON_TEXT = '❓ Правила'
SUPPORT_BUTTON_TEXT = '🤖 Обратиться в поддержку'

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=GAMES_BUTTON_TEXT), KeyboardButton(text=ENTERTAINMENTS_BUTTON_TEXT)],
        [KeyboardButton(text=RULES_BUTTON_TEXT)],
        [KeyboardButton(text=SUPPORT_BUTTON_TEXT)]
    ],
    resize_keyboard=True
)


async def send_keyboard(message: types.Message):
    await message.answer("Выберите пункт меню:", reply_markup=keyboard)


async def send_keyboard_by_chat_id(chat_id):
    bot = MyBot().getInstance()
    await bot.send_message(chat_id, "Выберите пункт меню:", reply_markup=keyboard)