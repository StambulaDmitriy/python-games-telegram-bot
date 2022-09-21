from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

import keyboards

BALANCE_BUTTON_TEXT = '💰 Баланс'
HALYAVA_BUTTON_TEXT = '🎁 Получить халяву'
BAGELS_BUTTON_TEXT = '👾 Багелс'
DICE_BUTTON_TEXT = '🎲 Кости'
ROULETTE_BUTTON_TEXT = '🧿 Рулетка'
BLACKJACK_BUTTON_TEXT = '🀄️ Блекджек'
RULES_BUTTON_TEXT = '❓ Правила'



keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=BALANCE_BUTTON_TEXT)],
        [KeyboardButton(text=HALYAVA_BUTTON_TEXT)],
        [KeyboardButton(text=BAGELS_BUTTON_TEXT), KeyboardButton(text=BLACKJACK_BUTTON_TEXT)],
        [KeyboardButton(text=DICE_BUTTON_TEXT), KeyboardButton(text=ROULETTE_BUTTON_TEXT)],
        [KeyboardButton(text=RULES_BUTTON_TEXT)],
        [KeyboardButton(text=keyboards.back_to_menu_keyboard.BACK_TO_MAINMENU_BUTTON_TEXT)]
    ],
    resize_keyboard=True
)


async def send_keyboard(message: types.Message):
    await message.answer("Выберите пункт меню:", reply_markup=keyboard)

