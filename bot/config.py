import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    ADMIN_CHAT_ID: int = int(os.getenv("ADMIN_CHAT_ID", "0"))
    GOOGLE_CREDENTIALS_FILE: str = os.getenv("GOOGLE_CREDENTIALS_FILE", "credentials.json")
    SPREADSHEET_NAME: str = os.getenv("SPREADSHEET_NAME", "Birthdays")
    SHEET_NAME: str = os.getenv("SHEET_NAME", "Лист1")
    DAYS_BEFORE: int = int(os.getenv("DAYS_BEFORE", "7"))
    REMINDER_HOUR: int = int(os.getenv("REMINDER_HOUR", "7"))
    REMINDER_MINUTE: int = int(os.getenv("REMINDER_MINUTE", "0"))
    TIMEZONE: str = os.getenv("TIMEZONE", "Europe/Moscow")


config = Config()

if not config.BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN не задан в .env")
