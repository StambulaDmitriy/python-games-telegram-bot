from aiogram.fsm.state import StatesGroup, State


class Magic8BallStates(StatesGroup):
    QuestionPending = State()
