from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

import keyboards.back_to_menu_keyboard

TODAY_PERIOD_BUTTON_TEXT = '〰️ На сегодня'
TOMORROW_PERIOD_BUTTON_TEXT = '🔜 На завтра'
SUBSCRIBE_BUTTON_TEXT = '🔔 Подписаться на рассылку'
UNSUBSCRIBE_BUTTON_TEXT = '🔕 Отписаться от рассылки'
CHANGE_ZODIAC_SIGN = "🔁 Изменить знак зодиака"


def get_keyboard_to_subscriber():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text=TODAY_PERIOD_BUTTON_TEXT), KeyboardButton(text=TOMORROW_PERIOD_BUTTON_TEXT)],
        [KeyboardButton(text=CHANGE_ZODIAC_SIGN)],
        [KeyboardButton(text=UNSUBSCRIBE_BUTTON_TEXT)],
        [KeyboardButton(text=keyboards.back_to_menu_keyboard.BACK_TO_MENU_BUTTON_TEXT)]
    ], resize_keyboard=True)


def get_keyboard_to_unsubscriber():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text=TODAY_PERIOD_BUTTON_TEXT), KeyboardButton(text=TOMORROW_PERIOD_BUTTON_TEXT)],
        [KeyboardButton(text=CHANGE_ZODIAC_SIGN)],
        [KeyboardButton(text=SUBSCRIBE_BUTTON_TEXT)],
        [KeyboardButton(text=keyboards.back_to_menu_keyboard.BACK_TO_MENU_BUTTON_TEXT)]
    ], resize_keyboard=True)
