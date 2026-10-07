from datetime import date, datetime
from typing import Optional

SUPPORTED_FORMATS = (
    "%d.%m.%Y",
    "%d.%m.%y",
    "%d.%m",
    "%d/%m/%Y",
    "%d/%m/%y",
    "%d/%m",
    "%Y-%m-%d",
)


def parse_date(date_str: str) -> Optional[date]:
    """Парсит строку в дату, поддерживая несколько форматов."""
    if not date_str:
        return None
    cleaned = date_str.strip()
    for fmt in SUPPORTED_FORMATS:
        try:
            dt = datetime.strptime(cleaned, fmt)
            # Для форматов без года подставляем 2000 (не влияет на расчёт дня)
            if "%Y" not in fmt and "%y" not in fmt:
                return date(2000, dt.month, dt.day)
            return dt.date()
        except ValueError:
            continue
    return None


def days_until_birthday(birthday: date, today: Optional[date] = None) -> int:
    """Сколько дней до ближайшего дня рождения (0 = сегодня)."""
    today = today or date.today()
    try:
        next_bd = birthday.replace(year=today.year)
    except ValueError:
        # 29 февраля в невисокосный год → считаем как 28 февраля
        next_bd = date(today.year, 2, 28)

    if next_bd < today:
        try:
            next_bd = birthday.replace(year=today.year + 1)
        except ValueError:
            next_bd = date(today.year + 1, 2, 28)

    return (next_bd - today).days


def format_date(date_str: str) -> str:
    """Приводит дату к единому виду ДД.ММ.ГГГГ или ДД.ММ."""
    cleaned = date_str.strip()
    for fmt in SUPPORTED_FORMATS:
        try:
            dt = datetime.strptime(cleaned, fmt)
            if "%Y" in fmt or "%y" in fmt:
                return dt.strftime("%d.%m.%Y")
            return dt.strftime("%d.%m")
        except ValueError:
            continue
    return cleaned
