from aiogram.filters.callback_data import CallbackData


class RulesCallbackData(CallbackData, prefix='rules'):
    game: str
