from datetime import datetime

from aiogram.fsm.storage.base import StorageKey
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import errors

from aiogram import types
from aiogram.fsm.context import FSMContext

import keyboards.main_menu_keyboard
from bootstrap import Database
from states.admin_support_states import AdminSupportStates
from states.user_support_states import UserSupportStates


async def user_initiates(message: types.Message, state: FSMContext):
    user_id = message.chat.id

    db = Database().getInstance()
    support_queue = db.casino.support_queue

    try:
        support_queue.insert_one({
            "_id": user_id,
            "created_at": datetime.now(),
        })
    except errors.DuplicateKeyError:
        await message.answer("Вы уже стоите в очереди")
        return

    await state.set_state(UserSupportStates.ConnectionPending)

    queue = support_queue.find({}).sort("created_at", 1)

    user_tuple = next(filter(lambda enum_tuple: enum_tuple[1]['_id'] == user_id, enumerate(queue)))

    queue_pos = user_tuple[0] + 1
    await message.answer(f"Ваш номер в очереди: {queue_pos}. Ожидайте подключения администратора...", reply_markup=types.ReplyKeyboardRemove())

    reply_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Подключиться", callback_data='support:next')]])
    await state.bot.send_message(642914377, f"<b>Новый пользователь в очереди на чат. Всего в очереди: {queue_pos}</b>\nКомманда для взаимодействия /next", reply_markup=reply_keyboard)


async def user_pending_connection(message: types.Message):
    user_id = message.from_user.id
    db = Database().getInstance()
    support_queue = db.casino.support_queue.find({}).sort("created_at", 1)
    user_tuple = next(filter(lambda enum_tuple: enum_tuple[1]['_id'] == user_id, enumerate(support_queue)))
    queue_pos = user_tuple[0] + 1
    await message.answer(f"Ожидайте подключения администратора. Ваша позиция в очереди: {queue_pos}")


async def user_cancel_chat(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = message.from_user.id
    if 'manager_id' in data:
        manager_id = data['manager_id']

        manager_state = FSMContext(state.bot, state.storage, StorageKey(bot_id=state.key.bot_id, chat_id=manager_id, user_id=manager_id))

        await manager_state.clear()
        await state.clear()

        await state.bot.send_message(manager_id, "<b>Пользователь покинул чат</b>")
    else:
        db = Database().getInstance()
        db.casino.support_queue.delete_one({"_id": user_id})
        await state.clear()

    await message.answer("Вы закончили чат")
    await message.answer("Выберите пункт меню:", reply_markup=keyboards.main_menu_keyboard.keyboard)

async def admin_accept(message: types.Message, state: FSMContext):
    db = Database().getInstance()
    support_queue = db.casino.support_queue

    if support_queue.count_documents({}) == 0:
        await message.answer("Очередь пустая")
        return

    supporting_user = next(support_queue.find({}).sort("created_at", 1))
    supporting_user_id = supporting_user["_id"]
    support_queue.delete_one({"_id": supporting_user_id})

    user_state = FSMContext(state.bot, state.storage, StorageKey(bot_id=state.key.bot_id, chat_id=supporting_user_id, user_id=supporting_user_id))

    await user_state.update_data(manager_id=message.chat.id)
    await user_state.set_state(UserSupportStates.Talking)

    await state.update_data(supporting_user_id=supporting_user_id)
    await state.set_state(AdminSupportStates.Talking)

    await message.answer("<b>Вы покдлючились к чату с пользователем</b>", reply_markup=types.ReplyKeyboardRemove())
    await state.bot.send_message(supporting_user_id, "<b>Администратор подключился к чату</b>")


async def admin_accept_inline(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await admin_accept(call.message, state)


async def admin_cancel_chat(message: types.Message, state: FSMContext):
    data = await state.get_data()
    supporting_user_id = data['supporting_user_id']

    user_state = FSMContext(state.bot, state.storage, StorageKey(bot_id=state.key.bot_id, chat_id=supporting_user_id, user_id=supporting_user_id))

    await user_state.clear()
    await state.clear()

    await message.answer("Вы закончили чат")
    await state.bot.send_message(supporting_user_id, "<b>Администратор покинул чат</b>")
    await state.bot.send_message(supporting_user_id, "Выберите пункт меню:", reply_markup=keyboards.main_menu_keyboard.keyboard)


async def admin_talking(message: types.Message, state: FSMContext):
    data = await state.get_data()
    supporting_user_id = data['supporting_user_id']

    await state.bot.send_message(supporting_user_id, f'<b>Администратор</b>\n{message.text}')


async def user_talking(message: types.Message, state: FSMContext):
    data = await state.get_data()
    manager_id = data['manager_id']

    await state.bot.send_message(manager_id, f'<b>{message.from_user.first_name} {message.from_user.last_name}</b>\n{message.text}')
