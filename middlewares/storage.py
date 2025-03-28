from aiogram.fsm.state import State, StatesGroup # Импортирование сохранений состояний

class UserLoreRead(StatesGroup):
    read = State()