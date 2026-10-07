from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from bot.Keyboards.main_menu import main_menu_kb

router = Router(name="start")


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(
        f"Привет, <b>{message.from_user.full_name}</b>! 👋\n\n"
        "Я помогу не забыть о днях рождения.\n"
        "Выберите действие в меню ниже 👇",
        reply_markup=main_menu_kb(),
    )


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    text = (
        "<b>Доступные команды:</b>\n\n"
        "/start — запустить бота\n"
        "/list — показать всех\n"
        "/add — добавить запись\n"
        "/delete — удалить запись\n"
        "/upcoming — ближайшие ДР\n"
        "/help — эта справка\n\n"
        "Напоминания приходят автоматически за "
        "несколько дней до события и в сам день рождения."
    )
    await message.answer(text, reply_markup=main_menu_kb())
