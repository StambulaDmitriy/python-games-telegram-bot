from aiogram.fsm.state import StatesGroup, State


class RouletteGameStates(StatesGroup):
    BetSumPending = State()
    BetPlacePending = State()
    ResultsPending = State()
