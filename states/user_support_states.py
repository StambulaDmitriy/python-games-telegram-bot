from aiogram.fsm.state import StatesGroup, State


class UserSupportStates(StatesGroup):
    ConnectionPending = State()
    Talking = State()
