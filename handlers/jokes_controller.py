import random

import aiohttp
from aiogram import types
from aiogram.fsm.context import FSMContext

import keyboards
from states.joke_states import JokeStates


async def joke_command(message: types.Message, state: FSMContext):
    await state.set_data({'social_raiting': 100})

    joke = await get_joke()

    await state.set_state(JokeStates.ReactionPending)
    await message.answer(joke, reply_markup=keyboards.joke_reaction_keyboard.keyboard)


async def return_to_menu(message: types.Message, state: FSMContext):
    await state.clear()
    await keyboards.entertainments_menu_keyboard.send_keyboard(message)


async def handle_reaction(message: types.Message, state: FSMContext):
    reaction = message.text
    if reaction not in [
        keyboards.joke_reaction_keyboard.AWFUL_REACTION_BUTTON_TEXT,
        keyboards.joke_reaction_keyboard.BAD_REACTION_BUTTON_TEXT,
        keyboards.joke_reaction_keyboard.NEUTRAL_REACTION_BUTTON_TEXT,
        keyboards.joke_reaction_keyboard.GOOD_REACTION_BUTTON_TEXT,
        keyboards.joke_reaction_keyboard.BEST_REACTION_BUTTON_TEXT
    ]:
        reaction = keyboards.joke_reaction_keyboard.NEUTRAL_REACTION_BUTTON_TEXT

    data = await state.get_data()
    social_raiting = data['social_raiting']

    if reaction == keyboards.joke_reaction_keyboard.AWFUL_REACTION_BUTTON_TEXT:
        social_raiting -= 25
    elif reaction == keyboards.joke_reaction_keyboard.BAD_REACTION_BUTTON_TEXT:
        social_raiting -= 12
    elif reaction == keyboards.joke_reaction_keyboard.NEUTRAL_REACTION_BUTTON_TEXT:
        pass
    elif reaction == keyboards.joke_reaction_keyboard.GOOD_REACTION_BUTTON_TEXT:
        social_raiting += 13
    elif reaction == keyboards.joke_reaction_keyboard.BEST_REACTION_BUTTON_TEXT:
        social_raiting += 25

    if social_raiting < 10:
        await message.answer("Да вы принцесса несмеяна! Вас не рассмешить. Подумайте над своим поведением и возвращайтесь позже")
        await return_to_menu(message, state)
        return

    await state.update_data(social_raiting=social_raiting)
    joke = await get_joke()

    await message.answer(joke)


async def get_joke():
    joke_category = [1, 11]
    async with aiohttp.ClientSession() as session:
        async with session.get('http://rzhunemogu.ru/RandJSON.aspx', params={'CType': random.choice(joke_category)}) as response:
            joke_in_abracadabra_format_by_stupid_developer = await response.text()

    joke = joke_in_abracadabra_format_by_stupid_developer.removeprefix("{\"content\":\"").removesuffix("\"}")
    joke = "\n".join(joke.splitlines())
    joke = "Внимание анекдот!\n\n" + joke

    return joke
