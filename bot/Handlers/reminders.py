from datetime import date

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.Services.sheets import sheets_service
from bot.Utils.date_utils import days_until_birthday, parse_date

router = Router(name="reminders")


@router.message(Command("upcoming"))
@router.message(F.text == "🔔 Ближайшие")
async def upcoming(message: Message) -> None:
    records = sheets_service.get_all()
    today = date.today()
    items = []

    for row in records:
        bd = parse_date(str(row.get("Дата рождения", "")))
        if not bd:
            continue
        diff = days_until_birthday(bd, today)
        items.append((diff, row.get("Имя", "—"), bd))

    if not items:
        await message.answer("Нет корректных записей для анализа.")
        return

    items.sort(key=lambda x: x[0])
    lines = ["<b>🔔 Ближайшие дни рождения:</b>\n"]
    for diff, name, bd in items[:15]:
        if diff == 0:
            when = "🎉 <b>сегодня!</b>"
        elif diff == 1:
            when = "завтра"
        else:
            when = f"через {diff} дн."
        lines.append(f"• <b>{name}</b> — {bd.strftime('%d.%m')} ({when})")

    await message.answer("\n".join(lines))
