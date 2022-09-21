from aiogram import types
from aiogram.fsm.context import FSMContext
import aiohttp
from bs4 import BeautifulSoup

import keyboards
from bootstrap import Database
from services import invert_dict
from states import HoroscopeStates

zodiac_signs = {
    keyboards.zodiak_signs_keyboard.ARIES_SIGN_BUTTON_TEXT: 'aries',
    keyboards.zodiak_signs_keyboard.TAURUS_SIGN_BUTTON_TEXT: 'taurus',
    keyboards.zodiak_signs_keyboard.GEMINI_SIGN_BUTTON_TEXT: 'gemini',
    keyboards.zodiak_signs_keyboard.CANCER_SIGN_BUTTON_TEXT: 'cancer',
    keyboards.zodiak_signs_keyboard.LEO_SIGN_BUTTON_TEXT: 'leo',
    keyboards.zodiak_signs_keyboard.VIRGO_SIGN_BUTTON_TEXT: 'virgo',
    keyboards.zodiak_signs_keyboard.LIBRA_SIGN_BUTTON_TEXT: 'libra',
    keyboards.zodiak_signs_keyboard.SCORPIO_SIGN_BUTTON_TEXT: 'scorpio',
    keyboards.zodiak_signs_keyboard.SAGITTARIUS_SIGN_BUTTON_TEXT: 'sagittarius',
    keyboards.zodiak_signs_keyboard.CAPRICORN_SIGN_BUTTON_TEXT: 'capricorn',
    keyboards.zodiak_signs_keyboard.AQUARIUS_SIGN_BUTTON_TEXT: 'aquarius',
    keyboards.zodiak_signs_keyboard.PISCES_SIGN_BUTTON_TEXT: 'pisces'
}

horoscope_periods = {
    keyboards.horoscope_period_keyboard.TODAY_PERIOD_BUTTON_TEXT: 'today',
    keyboards.horoscope_period_keyboard.TOMORROW_PERIOD_BUTTON_TEXT: 'tomorrow'
}


async def horoscope_command(message: types.Message, state: FSMContext):
    db = Database().getInstance()
    users_table = db.casino.users
    user = users_table.find_one({"_id": message.from_user.id})

    if user is None:
        await message.answer("Вы не начинали работу с ботом. Для начала введите команду /start")
        return

    if 'zodiak_sign' not in user:
        await select_zodiak_sign(message, state)
        return

    await select_horoscope_period(message, state)


async def select_zodiak_sign(message: types.Message, state: FSMContext):
    await state.set_state(HoroscopeStates.SelectingSign)
    await message.answer("Выберите ваш знак зодиака:", reply_markup=keyboards.zodiak_signs_keyboard.keyboard)


async def select_horoscope_period(message: types.Message, state: FSMContext):
    await state.set_state(HoroscopeStates.SelectingPeriod)
    await message.answer("Выберите период гороскопа:", reply_markup=keyboards.horoscope_period_keyboard.keyboard)


async def return_to_menu(message: types.Message, state: FSMContext):
    await state.clear()
    await keyboards.entertainments_menu_keyboard.send_keyboard(message)


async def handle_zodiak_sign(message: types.Message, state: FSMContext):
    sign_text = message.text

    if sign_text not in [
        keyboards.zodiak_signs_keyboard.ARIES_SIGN_BUTTON_TEXT,
        keyboards.zodiak_signs_keyboard.TAURUS_SIGN_BUTTON_TEXT,
        keyboards.zodiak_signs_keyboard.GEMINI_SIGN_BUTTON_TEXT,
        keyboards.zodiak_signs_keyboard.CANCER_SIGN_BUTTON_TEXT,
        keyboards.zodiak_signs_keyboard.LEO_SIGN_BUTTON_TEXT,
        keyboards.zodiak_signs_keyboard.VIRGO_SIGN_BUTTON_TEXT,
        keyboards.zodiak_signs_keyboard.LIBRA_SIGN_BUTTON_TEXT,
        keyboards.zodiak_signs_keyboard.SCORPIO_SIGN_BUTTON_TEXT,
        keyboards.zodiak_signs_keyboard.SAGITTARIUS_SIGN_BUTTON_TEXT,
        keyboards.zodiak_signs_keyboard.CAPRICORN_SIGN_BUTTON_TEXT,
        keyboards.zodiak_signs_keyboard.AQUARIUS_SIGN_BUTTON_TEXT,
        keyboards.zodiak_signs_keyboard.PISCES_SIGN_BUTTON_TEXT
    ]:
        await message.answer("Невалидный знак зодиака. Выберите ваш знак из меню ниже")
        await select_zodiak_sign(message, state)
        return

    db = Database().getInstance()
    users_table = db.casino.users
    users_table.update_one({"_id": message.from_user.id},{
        "$set": {
            'zodiak_sign': zodiac_signs[sign_text]
        }
    })

    await select_horoscope_period(message, state)


async def handle_horoscope_period(message: types.Message, state: FSMContext):
    horoscope_period = message.text

    if horoscope_period not in [
        keyboards.horoscope_period_keyboard.TODAY_PERIOD_BUTTON_TEXT,
        keyboards.horoscope_period_keyboard.TOMORROW_PERIOD_BUTTON_TEXT
    ]:
        await message.answer("Невалидный период гороскопа. Выберите период из меню ниже")
        await select_horoscope_period(message, state)
        return

    db = Database().getInstance()
    users_table = db.casino.users
    user = users_table.find_one({"_id": message.from_user.id})

    if 'zodiak_sign' not in user:
        await select_zodiak_sign(message, state)
        return

    zodiak_sign = user['zodiak_sign']

    horoscope_prediction = await get_horoscope(zodiak_sign, horoscope_periods[horoscope_period])

    result_string = "Гороскоп <b>{}</b> для знака зодиака: {}\n".format(horoscope_period.lower(), invert_dict(zodiac_signs)[zodiak_sign])

    result_string += horoscope_prediction

    await message.answer(result_string)
    await select_horoscope_period(message, state)


async def get_horoscope(zodiak_sign, horoscope_period):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://horo.mail.ru/prediction/{zodiak_sign}/{horoscope_period}/'.format(zodiak_sign=zodiak_sign, horoscope_period=horoscope_period)) as response:
            html = await response.text()

            parser = BeautifulSoup(html, 'html.parser')
            selected_tags = parser.select("div.article_prediction div.article__text div.article__item p")

            selected_paragraphs = map(lambda el: el.string, selected_tags)

            result = "\n\n".join(selected_paragraphs)

    return result
