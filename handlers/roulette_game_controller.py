import asyncio
import random

from aiogram import types
from aiogram.fsm.context import FSMContext

import keyboards
from bootstrap import Database
from services import validate_bet
from states.roulette_game_states import RouletteGameStates


async def start(message: types.Message, state: FSMContext):
    await message.answer("Введите ставку:", reply_markup=keyboards.back_to_menu_keyboard.keyboard)
    await state.set_state(RouletteGameStates.BetSumPending)


async def return_to_menu(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Выберите пункт меню:", reply_markup=keyboards.main_menu_keyboard.keyboard)


async def return_to_bet(message: types.Message, state: FSMContext):
    await state.set_data({})
    await start(message, state)


async def handle_bet_sum(message: types.Message, state: FSMContext):
    db = Database().getInstance()
    users_table = db.casino.users

    user = users_table.find_one({"_id": message.from_user.id})

    if user is None:
        await message.answer("Вы не начинали работу с ботом. Для начала введите команду /start")
        return

    bet_validating_res = validate_bet(message.text, user['balance'])

    if bet_validating_res != True:
        await message.answer(bet_validating_res)
        await start(message, state)
        return

    bet = int(message.text)

    await state.update_data(bet=bet)
    await state.set_state(RouletteGameStates.BetPlacePending)

    await ask_bet_place(message, state)


async def ask_bet_place(message: types.Message, state: FSMContext):
    await message.answer("На что ставим? Выберите вариант из меню или введите конкретное число:", reply_markup=keyboards.roulette_bet_places_keyboard.keyboard)


def is_valid_bet_place(bet_place):
    if bet_place in [
        keyboards.roulette_bet_places_keyboard.BLACK_PLACE_BUTTON_TEXT,
        keyboards.roulette_bet_places_keyboard.RED_PLACE_BUTTON_TEXT,
        keyboards.roulette_bet_places_keyboard.FIRST_COLUMN_PLACE_BUTTON_TEXT,
        keyboards.roulette_bet_places_keyboard.SECOND_COLUMN_PLACE_BUTTON_TEXT,
        keyboards.roulette_bet_places_keyboard.THIRD_COLUMN_PLACE_BUTTON_TEXT,
        keyboards.roulette_bet_places_keyboard.FIRST_HALF_PLACE_BUTTON_TEXT,
        keyboards.roulette_bet_places_keyboard.SECOND_HALF_PLACE_BUTTON_TEXT,
    ]:
        return True

    if bet_place.isdigit() and 0 <= int(bet_place) <= 36:
        return True

    return False


async def handle_bet_place(message: types.Message, state: FSMContext):
    if not is_valid_bet_place(message.text):
        await message.answer("Данная ставка невозможна")
        await ask_bet_place(message, state)
        return

    bet_place = message.text
    await state.set_state(RouletteGameStates.ResultsPending)
    await message.answer("Ставки приняты. Ставок больше нет.\nДиллер раскручивает рулетку...")
    await state.bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(3)

    spin_result = random.randint(0, 36)
    if spin_result == 0:
        spin_result_text = "0 - зиро!"
    elif spin_result % 2 == 0:
        spin_result_text = f"{spin_result} - 🔴"
    else:
        spin_result_text = f"{spin_result} - ⚫"

    x = {'0': '0️⃣', '1': '1️⃣', '2': '2️⃣', '3': '3️⃣', '4': '4️⃣', '5': '5️⃣', '6': '6️⃣', '7': '7️⃣', '8': '8️⃣', '9': '9️⃣'}
    tbl = spin_result_text.maketrans(x)
    spin_result_text = spin_result_text.translate(tbl)

    await message.answer(spin_result_text)
    await asyncio.sleep(3)

    win_places = {spin_result: 36}

    if spin_result != 0:
        if spin_result % 2 == 0:
            win_places[keyboards.roulette_bet_places_keyboard.RED_PLACE_BUTTON_TEXT] = 2
        else:
            win_places[keyboards.roulette_bet_places_keyboard.BLACK_PLACE_BUTTON_TEXT] = 2

        if spin_result in range(1,19):
            win_places[keyboards.roulette_bet_places_keyboard.FIRST_HALF_PLACE_BUTTON_TEXT] = 2
        else:
            win_places[keyboards.roulette_bet_places_keyboard.SECOND_HALF_PLACE_BUTTON_TEXT] = 2

        if spin_result in range(1, 37, 3):
            win_places[keyboards.roulette_bet_places_keyboard.FIRST_COLUMN_PLACE_BUTTON_TEXT] = 3
        elif spin_result in range(2, 37, 3):
            win_places[keyboards.roulette_bet_places_keyboard.SECOND_COLUMN_PLACE_BUTTON_TEXT] = 3
        elif spin_result in range(3, 37, 3):
            win_places[keyboards.roulette_bet_places_keyboard.THIRD_COLUMN_PLACE_BUTTON_TEXT] = 3

    data = await state.get_data()
    bet = data['bet']

    if bet_place not in win_places:
        balance_change = -bet
        await message.answer(f"⚰️Ваша ставка не сыграла! Вы проиграли ${bet}")
    else:
        koef = win_places[bet_place]
        balance_change = bet * koef
        await message.answer(f"🥳 Ваша ставка сыграла! Вы выиграли ${bet * koef}")

    client = Database().getInstance()
    client.casino.users.update_one({"_id": message.from_user.id}, {
        "$inc": {
            "balance": balance_change
        }
    })

    await state.set_data({})

    await start(message, state)
