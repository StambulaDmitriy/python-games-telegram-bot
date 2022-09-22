from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

import keyboards.back_to_menu_keyboard


AWFUL_REACTION_BUTTON_TEXT = "🤮"
BAD_REACTION_BUTTON_TEXT = "🙁"
NEUTRAL_REACTION_BUTTON_TEXT = "😐"
GOOD_REACTION_BUTTON_TEXT = "🙂"
BEST_REACTION_BUTTON_TEXT = "🤣"

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=AWFUL_REACTION_BUTTON_TEXT),
            KeyboardButton(text=BAD_REACTION_BUTTON_TEXT),
            KeyboardButton(text=NEUTRAL_REACTION_BUTTON_TEXT),
            KeyboardButton(text=GOOD_REACTION_BUTTON_TEXT),
            KeyboardButton(text=BEST_REACTION_BUTTON_TEXT),
        ],
        [KeyboardButton(text=keyboards.back_to_menu_keyboard.BACK_TO_MENU_BUTTON_TEXT)]
    ],
    resize_keyboard=True
)