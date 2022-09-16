import asyncio
import random

from aiogram import types
from aiogram.fsm.context import FSMContext

import keyboards
from bootstrap import Database
from services import validate_bet
from states.blackjack_game_states import BlackjackGameStates


async def start(message: types.Message, state: FSMContext):
    await message.answer("Введите ставку:", reply_markup=keyboards.back_to_menu_keyboard.keyboard)
    await state.set_state(BlackjackGameStates.BetPending)


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

    deck = get_deck()
    user_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]

    await state.update_data(deck=deck, user_hand=user_hand, dealer_hand=dealer_hand, bet=bet)
    await state.set_state(BlackjackGameStates.UserPlaying)

    await message.answer('Ставка принята. Диллер раздаёт карты... Первая карта диллера изначально скрыта', reply_markup=types.ReplyKeyboardRemove())

    await show_cards_and_ask_user_choice(message, state)


async def show_cards_and_ask_user_choice(message: types.Message, state: FSMContext):
    data = await state.get_data()

    user_hand = data['user_hand']
    dealer_hand = data['dealer_hand']

    await message.answer('\n'.join(get_display_hands(user_hand, dealer_hand, False)))

    if get_hand_value(user_hand) >= 21:
        await blackjack_check_result(message, state)
        return

    await message.answer("Ваш ход:", reply_markup=keyboards.blackjack_menu_keyboard.keyboard)


async def handle_user_choice(message: types.Message, state: FSMContext):
    if message.text not in [
        keyboards.blackjack_menu_keyboard.HIT_BUTTON_TEXT,
        keyboards.blackjack_menu_keyboard.STAND_BUTTON_TEXT,
    ]:
        await message.answer("♿️ Такой ход сделать нельзя!")
        await show_cards_and_ask_user_choice(message, state)
        return

    if message.text == keyboards.blackjack_menu_keyboard.HIT_BUTTON_TEXT:
        data = await state.get_data()
        new_card = data['deck'].pop()
        data['user_hand'].append(new_card)
        await message.answer("Вы взяли {} {}".format(new_card[0], new_card[1]))
        await state.set_data(data)

        await show_cards_and_ask_user_choice(message, state)
    else:
        await blackjack_check_result(message, state)


async def blackjack_check_result(message: types.Message, state: FSMContext):
    data = await state.get_data()

    deck = data['deck']
    user_hand = data['user_hand']
    dealer_hand = data['dealer_hand']
    bet = data['bet']

    if get_hand_value(user_hand) < 21:
        await state.set_state(BlackjackGameStates.DealerPlaying)
        await message.answer("Диллер раскрывает первую карту")
        await message.answer("\n".join(get_display_hands(user_hand, dealer_hand, True)))
        await asyncio.sleep(3)
        while get_hand_value(dealer_hand) < 17:
            dealer_hand.append(deck.pop())
            await message.answer("У Диллера на руках меньше 17. Берёт ещё одну карту...")
            await message.answer("\n".join(get_display_hands(user_hand, dealer_hand, True)))
            await asyncio.sleep(3)

    player_value = get_hand_value(user_hand)
    dealer_value = get_hand_value(dealer_hand)

    balance_change = 0
    if player_value == 21:
        await message.answer(f"🥳 У вас очко! Вы выиграли ${bet*2}")
        balance_change = bet*2
    elif dealer_value > 21:
        await message.answer(f'🥳 Диллер перебрал карт! Вы выиграли ${bet*2}!')
        balance_change = bet*2
    elif player_value > 21:
        await message.answer(f'⚰️ Вы перебрали карт! Вы проиграли ${bet}!')
        balance_change = -bet
    elif player_value < dealer_value:
        await message.answer(f'⚰️ Диллер набрал больше очков! Вы проиграли ${bet}!')
        balance_change = -bet
    elif player_value > dealer_value:
        await message.answer(f'🥳 Вы набрали больше диллера! Вы выиграли ${bet*2}!')
        balance_change = bet*2
    elif player_value == dealer_value:
        await message.answer('😕 Ничья... Ставки возвращаются')
        balance_change = 0

    client = Database().getInstance()
    client.casino.users.update_one({"_id": message.from_user.id}, {
        "$inc": {
            "balance": balance_change
        }
    })

    await state.set_data({})

    await start(message, state)


def get_deck():
    """Возвращаем список кортежей (номинал, масть) для всех 52 карт."""
    deck = []
    for suit in ('♠', '♣', '♥', '♦'):
        for rank in range(2, 11):
            deck.append((str(rank), suit)) # Добавляем числовые карты.
        for rank in ('J', 'Q', 'K', 'A'):
            deck.append((rank, suit)) # Добавляем фигурные карты и тузы.
    random.shuffle(deck)
    return deck


def get_display_hands(user_hand, dealer_hand, showFirstCard):
    rows = []
    if not showFirstCard:
        rows.append("Карты диллера (очков: ???):")
    else:
        rows.append(f"Карты диллера (очков: {get_hand_value(dealer_hand)}):")

    rows += get_display_cards(dealer_hand, showFirstCard)

    rows.append(f'Ваши карты (очков: {get_hand_value(user_hand)}):')
    rows += get_display_cards(user_hand, True)

    return rows


def get_display_cards(cards, showFirstCard):
    """Отображаем все карты из списка карт."""
    rows = ['', '', '', '', ''] # Отображаемый в каждой строке текст.

    for i, card in enumerate(cards):
        rows[0] += ' ____  ' # Выводим верхнюю строку карты.
        if i == 0 and showFirstCard is False:
            rows[1] += '|##  | '
            rows[2] += '| ## | '
            rows[3] += '|__##| '
        else:
            rank, suit = card
            rows[1] += '|{}  | '.format(rank.ljust(2))
            rows[2] += '| {} | '.format(suit)
            rows[3] += '|__{}| '.format(rank.rjust(2, '_'))

    for i in range(4):
        rows[i] = '<code>' + rows[i] + '</code>'

    return rows


def get_hand_value(cards):
    """ Возвращаем стоимость карт. Фигурные карты стоят 10, тузы — 11
    или 1 очко (эта функция выбирает подходящую стоимость карты)."""
    value = 0
    numberOfAces = 0

    # Добавляем стоимость карты — не туза:
    for card in cards:
        rank = card[0] # карта представляет собой кортеж (номинал, масть)
        if rank == 'A':
            numberOfAces += 1
        elif rank in ('K', 'Q', 'J'): # Фигурные карты стоят 10 очков.
            value += 10
        else:
            value += int(rank) # Стоимость числовых карт равна их номиналу.

    # Добавляем стоимость для тузов:
    value += numberOfAces # Добавляем 1 для каждого туза.
    for i in range(numberOfAces):
    # Если можно добавить еще 10 с перебором, добавляем:
        if value + 10 <= 21:
            value += 10

    return value

