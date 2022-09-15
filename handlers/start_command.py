from datetime import datetime

from aiogram import types

import keyboards
from bootstrap import Database


async def start(message: types.Message):
    db = Database().getInstance()
    users_table = db.casino.users

    user = users_table.find_one({"_id": message.from_user.id})

    if user is None:
        users_table.insert_one({
            "_id": message.from_user.id,
            "balance": 1000,
            "created_at": datetime.now(),
            "halyava_available_at": datetime.now(),
        })
        await message.answer(
            f"Добро пожаловать в игровой бот.")

    await message.answer("Выберите пункт меню:", reply_markup=keyboards.main_menu_keyboard)
