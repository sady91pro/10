from aiogram.fsm.state import State, StatesGroup


class AddBirthday(StatesGroup):
    waiting_name = State()
    waiting_date = State()
    waiting_extra = State()


class DeleteBirthday(StatesGroup):
    waiting_name = State()
