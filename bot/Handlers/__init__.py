from aiogram import Dispatcher

from . import start, birthdays, reminders


def register_all_handlers(dp: Dispatcher) -> None:
    dp.include_router(start.router)
    dp.include_router(birthdays.router)
    dp.include_router(reminders.router)
