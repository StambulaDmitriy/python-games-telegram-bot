from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

BALANCE_BUTTON_TEXT = '💰 Баланс'
HALYAVA_BUTTON_TEXT = '🎁 Получить халяву'
BAGELS_BUTTON_TEXT = '👾 Багелс'
DICE_BUTTON_TEXT = '🎲 Кости'
ROULETTE_BUTTON_TEXT = '🧿 Рулетка'
BLACKJACK_BUTTON_TEXT = '🀄️ Блекджек'
RULES_BUTTON_TEXT = '❓ Правила'
SUPPORT_BUTTON_TEXT = '🤖 Обратиться в поддержку'

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=BALANCE_BUTTON_TEXT)],
        [KeyboardButton(text=HALYAVA_BUTTON_TEXT)],
        [KeyboardButton(text=BAGELS_BUTTON_TEXT)],
        [KeyboardButton(text=DICE_BUTTON_TEXT), KeyboardButton(text=ROULETTE_BUTTON_TEXT), KeyboardButton(text=BLACKJACK_BUTTON_TEXT)],
        [KeyboardButton(text=RULES_BUTTON_TEXT)],
        [KeyboardButton(text=SUPPORT_BUTTON_TEXT)]
    ],
    resize_keyboard=True
)
