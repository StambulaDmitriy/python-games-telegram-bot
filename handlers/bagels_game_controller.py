import random
import re

from aiogram import types
from aiogram.fsm.context import FSMContext

import keyboards
from bootstrap import Database
from services import validate_bet
from states import BagelsGameStates


def generate_secret(num_length):
    return "".join(random.choices("0123456789", k=num_length))


async def start(message: types.Message, state: FSMContext):
    await message.answer("Введите ставку:", reply_markup=keyboards.back_to_menu_keyboard.keyboard)
    await state.set_state(BagelsGameStates.BetPending)


async def return_to_menu(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Выберите пункт меню:", reply_markup=keyboards.main_menu_keyboard.keyboard)


async def handle_bet(message: types.Message, state: FSMContext):
    db = Database().getInstance()
    users_table = db.casino.users

    user = users_table.find_one({"_id": message.from_user.id})

    if user is None:
        await message.answer("Вы не начинали работу с ботом. Для начала введите команду /start", reply_markup=types.ReplyKeyboardRemove())
        return

    bet_validating_res = validate_bet(message.text, user['balance'])

    if bet_validating_res != True:
        await message.answer(bet_validating_res)
        await start(message, state)
        return

    bet = int(message.text)

    secret_num = generate_secret(3)

    await state.update_data(secret_num=secret_num, available_attempts=10, bet=bet)
    await state.set_state(BagelsGameStates.NumberGuessing)

    await message.answer('Я загадал 3-х значное число! У тебя есть 10 попыток его угадать:', reply_markup=types.ReplyKeyboardRemove())


async def check_answer(message: types.Message, state: FSMContext):
    regexp = re.compile(r"^[0-9]{3}$")

    answer = message.text

    if not regexp.match(answer):
        await message.answer("♿️ Нужно ввести 3-х значное число!")
        return

    hints = []
    data = await state.get_data()
    secret_num = data['secret_num']
    bet = data['bet']
    available_attempts = data['available_attempts']

    if secret_num == answer:
        await message.answer(f"🥳 Ты угадал! Твой выигрыш составляет <b>${data['bet']*2}</b>")

        client = Database().getInstance()
        client.casino.users.update_one({"_id": message.from_user.id}, {
            "$inc": {
                "balance": bet*2
            }
        })

        await state.clear()
        await start(message, state)
        return

    for i in range(len(secret_num)):
        if answer[i] == secret_num[i]:
            hints.append("Горячо")
        elif answer[i] in secret_num:
            hints.append("Тепло")

    if len(hints) < 1:
        hints.append("Холодно")

    hints.sort()
    hints_txt = " ".join(hints)

    await message.answer(f"😢 Не угадал!\nВот мои подсказки: {hints_txt}")

    available_attempts -= 1

    if available_attempts <= 0:
        await message.answer(f"♿️ Попытки закончились. Ты проиграл <b>${bet}</b>\nЗагадонное число было: {secret_num}")
        client = Database().getInstance()
        client.casino.users.update_one({"_id": message.from_user.id}, {
            "$inc": {
                "balance": -bet
            }
        })

        await state.clear()
        await start(message, state)
        return

    await state.update_data(available_attempts=available_attempts)

    await message.answer(f"Осталось попыток: {available_attempts}")

