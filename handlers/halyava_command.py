from datetime import datetime, timedelta, timezone
import random

from aiogram import types

import keyboards.main_menu_keyboard
from bootstrap import Database


async def halyava_command(message: types.Message):
    db = Database().getInstance()
    users_table = db.casino.users

    user = users_table.find_one({"_id": message.from_user.id})

    if user is None:
        await message.answer("Вы не начинали работу с ботом. Для начала введите команду /start")
        return

    halyava_available_at = user['halyava_available_at']

    if halyava_available_at < datetime.now():
        halyava_size = random.randint(10, 20) * 100
        halyava_available_at = datetime.now() + timedelta(minutes=15)

        users_table.update_one({
            "_id": user['_id']
        }, {
            "$inc": {
                "balance": halyava_size,
            },
            "$set": {
                "halyava_available_at": halyava_available_at,
            }
        })

        await message.answer(f"Вам досталось нахаляву: <b>${halyava_size}</b>")
    else:
        await message.answer("Следующая халява будет доступна " + halyava_available_at.astimezone(timezone(timedelta(hours=3), name='Europe/Moscow')).strftime("%d.%m.%Y в %H:%M:%S"))

    await message.answer("Выберите пункт меню:", reply_markup=keyboards.main_menu_keyboard.keyboard)

