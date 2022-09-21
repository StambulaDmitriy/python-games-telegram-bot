import random

from aiogram import types
from aiogram.fsm.context import FSMContext

import keyboards
from states import Magic8BallStates

answers = [
    'Бесспорно',
    'Предрешено',
    'Никаких сомнений',
    'Определённо да',
    'Можешь быть уверен в этом',
    'Мне кажется — «да»',
    'Вероятнее всего',
    'Хорошие перспективы',
    'Знаки говорят — «да»',
    'Да',
    'Пока не ясно, попробуй снова',
    'Спроси позже',
    'Лучше не рассказывать',
    'Сейчас нельзя предсказать',
    'Сконцентрируйся и спроси опять',
    'Даже не думай',
    'Мой ответ — «нет»',
    'По моим данным — «нет»',
    'Перспективы не очень хорошие',
    'Весьма сомнительно'
]


async def start(message: types.Message, state: FSMContext):
    await state.set_state(Magic8BallStates.QuestionPending)
    await message.answer("Задай мне вопрос. Постарайся, чтобы он был чётким, и не воспринимался двойственно.", reply_markup=keyboards.back_to_menu_keyboard.to_submenu_keyboard)


async def answer(message: types.Message):
    await message.answer(random.choice(answers), reply_markup=keyboards.back_to_menu_keyboard.to_submenu_keyboard)


async def return_to_menu(message: types.Message, state: FSMContext):
    await state.clear()
    await keyboards.entertainments_menu_keyboard.send_keyboard(message)

