from aiogram.filters.callback_data import CallbackData


class HelpCallbackData(CallbackData, prefix='help'):
    game: str
