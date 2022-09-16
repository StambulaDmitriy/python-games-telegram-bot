from aiogram.fsm.state import StatesGroup, State


class BlackjackGameStates(StatesGroup):
    BetPending = State()
    UserPlaying = State()
    DealerPlaying = State()
