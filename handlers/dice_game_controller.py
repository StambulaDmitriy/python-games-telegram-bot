import asyncio

from aiogram import types
from aiogram.fsm.context import FSMContext

import keyboards
from bootstrap import Database
from services import validate_bet
from states import DiceGameStates


async def start(message: types.Message, state: FSMContext):
    await message.answer("Введите ставку:", reply_markup=keyboards.back_to_menu_keyboard.keyboard)
    await state.set_state(DiceGameStates.BetPending)


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

    await state.set_state(DiceGameStates.ResultsPending)

    await message.answer("Ставка принята.\nДиллер бросает кость первым:", reply_markup=types.ReplyKeyboardRemove())
    dealer_result_message = await message.answer_dice(types.dice.DiceEmoji.DICE)
    await asyncio.sleep(3)

    await message.answer("Вы бросаете кости:")
    user_result_message = await message.answer_dice(types.dice.DiceEmoji.DICE)
    await asyncio.sleep(5)

    dealer_res = dealer_result_message.dice.value
    user_res = user_result_message.dice.value

    answer = f"Вам выпало {user_res}, а диллеру {dealer_res}\n\n"

    if dealer_res > user_res:
        answer += f"⚰️ Вы проиграли <b>${bet}!</b>"
        balance_change = -bet
    elif user_res > dealer_res:
        answer += f"🥳 Вы выиграли <b>${bet}!</b>"
        balance_change = bet
    else:
        answer += "😕 Ничья! Ставка возвращена."
        balance_change = 0

    db = Database().getInstance()
    db.casino.users.update_one({"_id": message.from_user.id}, {
        "$inc": {
            "balance": balance_change
        }
    })

    await message.answer(answer)

    await state.clear()

    await start(message, state)
