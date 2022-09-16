from aiogram.fsm.state import StatesGroup, State


class BagelsGameStates(StatesGroup):
    BetPending = State()
    NumberGuessing = State()
    ResultsPending = State()
