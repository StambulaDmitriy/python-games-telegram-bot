from aiogram import types

import keyboards.main_menu_keyboard
from bootstrap import Database


async def balance_command(message: types.Message):
    db = Database().getInstance()
    users_table = db.casino.users

    user = users_table.find_one({"_id": message.from_user.id})

    if user is None:
        await message.answer("Вы не начинали работу с ботом. Для начала введите команду /start")
        return

    await message.answer(f"Ваш баланс: <b>${user['balance']}</b>")
    await message.answer("Выберите пункт меню:", reply_markup=keyboards.main_menu_keyboard.keyboard)
