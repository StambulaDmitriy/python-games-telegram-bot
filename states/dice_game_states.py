from aiogram.fsm.state import StatesGroup, State


class DiceGameStates(StatesGroup):
    BetPending = State()
    ResultsPending = State()
