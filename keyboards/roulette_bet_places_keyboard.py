from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

RED_PLACE_BUTTON_TEXT = '🔴 Красное'
BLACK_PLACE_BUTTON_TEXT = '⚫ Черное'
FIRST_COLUMN_PLACE_BUTTON_TEXT = '🥇 Первая колонка'
SECOND_COLUMN_PLACE_BUTTON_TEXT = '🥈 Вторая колонка'
THIRD_COLUMN_PLACE_BUTTON_TEXT = '🥉 Третья колонка'
FIRST_HALF_PLACE_BUTTON_TEXT = '🔼 Первая половина'
SECOND_HALF_PLACE_BUTTON_TEXT = '🔽 Вторая половина'
BACK_TO_CHOOSE_BET_SUM = '🔙 Назад к выбору ставки'

keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=RED_PLACE_BUTTON_TEXT), KeyboardButton(text=BLACK_PLACE_BUTTON_TEXT)],
    [KeyboardButton(text=FIRST_COLUMN_PLACE_BUTTON_TEXT), KeyboardButton(text=SECOND_COLUMN_PLACE_BUTTON_TEXT), KeyboardButton(text=THIRD_COLUMN_PLACE_BUTTON_TEXT)],
    [KeyboardButton(text=FIRST_HALF_PLACE_BUTTON_TEXT), KeyboardButton(text=SECOND_HALF_PLACE_BUTTON_TEXT)],
    [KeyboardButton(text=BACK_TO_CHOOSE_BET_SUM)],
])
