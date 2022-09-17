from aiogram.fsm.state import StatesGroup, State


class HoroscopeStates(StatesGroup):
    SelectingSign = State()
    SelectingPeriod = State()
