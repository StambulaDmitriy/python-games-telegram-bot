from aiogram.fsm.state import StatesGroup, State


class JokeStates(StatesGroup):
    ReactionPending = State()
