from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def main_menu_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📋 Список"), KeyboardButton(text="➕ Добавить")],
            [KeyboardButton(text="🔔 Ближайшие"), KeyboardButton(text="🗑 Удалить")],
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите действие...",
    )
