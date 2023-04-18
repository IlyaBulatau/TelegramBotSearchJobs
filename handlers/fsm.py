from aiogram.fsm.state import State, StatesGroup

class JobsForm(StatesGroup):
    """
    Класс FSM  для составления запроса
    """
    job = State()
    sort = State()
    count = State()
