from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

ARIES_SIGN_BUTTON_TEXT = '♈️ Овен'
TAURUS_SIGN_BUTTON_TEXT = '♉️ Телец'
GEMINI_SIGN_BUTTON_TEXT = '♊️ Близнецы'
CANCER_SIGN_BUTTON_TEXT = '♋️ Рак'
LEO_SIGN_BUTTON_TEXT = '♌️ Лев'
VIRGO_SIGN_BUTTON_TEXT = '♍️ Дева'
LIBRA_SIGN_BUTTON_TEXT = '♎️ Весы'
SCORPIO_SIGN_BUTTON_TEXT = '♏️ Скорпион'
SAGITTARIUS_SIGN_BUTTON_TEXT = '♐️ Стрелец'
CAPRICORN_SIGN_BUTTON_TEXT = '♑️ Козерог'
AQUARIUS_SIGN_BUTTON_TEXT = '♒️ Водолей'
PISCES_SIGN_BUTTON_TEXT = '♓️ Рыбы'

keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=ARIES_SIGN_BUTTON_TEXT), KeyboardButton(text=TAURUS_SIGN_BUTTON_TEXT)],
    [KeyboardButton(text=GEMINI_SIGN_BUTTON_TEXT), KeyboardButton(text=CANCER_SIGN_BUTTON_TEXT)],
    [KeyboardButton(text=LEO_SIGN_BUTTON_TEXT), KeyboardButton(text=VIRGO_SIGN_BUTTON_TEXT)],
    [KeyboardButton(text=LIBRA_SIGN_BUTTON_TEXT), KeyboardButton(text=SCORPIO_SIGN_BUTTON_TEXT)],
    [KeyboardButton(text=SAGITTARIUS_SIGN_BUTTON_TEXT), KeyboardButton(text=CAPRICORN_SIGN_BUTTON_TEXT)],
    [KeyboardButton(text=AQUARIUS_SIGN_BUTTON_TEXT), KeyboardButton(text=PISCES_SIGN_BUTTON_TEXT)],
])
