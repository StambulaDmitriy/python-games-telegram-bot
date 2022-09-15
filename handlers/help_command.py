from aiogram import types

import keyboards
from keyboards.inline import HelpCallbackData


def get_games_rules():
    return {
        'dice': "Правила игры в кости: Диллер и вы по очереди бросаете кости. Побеждает тот, у кого выпало большее число. При выигрыше ставка X2. При ничьей ставка возвращается.",
        'roulette': "Правила игры в рулетку: За ставку на правильный цвет Х2, за ставку на правильную половину Х2, за ставку на правильную колонку Х3, за ставку на правильное число Х36",
        'bagels': "Правила игры Багелс: Необходимо угадать 3-х значное число за 10 попыток опираясь на подсказки:\nГорячо -  одна цифра правильная и на своей позиции;\nТепло - одна цифра правильная, но не на своей позиции;\nХолодно - все цифры неправильные;\nПодсказки даются в произвольном порядке следования",
        'blackjack': "Правила игры в Блекджек: Цель игры добирать в руку карты и набрать больше очков, чем диллер, но не более 21. Короли, Дамы и Валеты стоят 10 очков. Тузы оцениваются по ситуации: Если в руку помещается 11 очков - туз оценивается в 11 очков, если не помещается - в 1 очко. Карты с 2 до 10 стоят своего номинала.\nВ случае победы ставка Х2, при ничьей ставка возвращается",
    }


async def help_command(message: types.Message):
    await message.answer('Выбери игру по которой необходима информация:', reply_markup=keyboards.inline.help_inline_keyboard)


async def help_inline_callback(call: types.CallbackQuery, callback_data: HelpCallbackData):
    await call.message.edit_text(get_games_rules()[callback_data.game], reply_markup=keyboards.inline.help_inline_keyboard)
    await call.answer()

