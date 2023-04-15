from aiogram.fsm.state import State, StatesGroup

class JobsForm(StatesGroup):
    job = State()
    sort = State()
    count = State()