from aiogram.filters import BaseFilter
from aiogram import types

from config import config


class IsAdmin(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        return message.from_user.id in config('admins')
