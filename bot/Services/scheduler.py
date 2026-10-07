import logging
from datetime import date

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from bot.config import config
from bot.Services.sheets import sheets_service
from bot.Utils.date_utils import days_until_birthday, parse_date

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler(timezone=config.TIMEZONE)


async def check_birthdays(bot: Bot) -> None:
    """Проверяет список и отправляет напоминания в ADMIN_CHAT_ID."""
    if not config.ADMIN_CHAT_ID:
        logger.warning("ADMIN_CHAT_ID не задан — напоминания не будут отправлены.")
        return

    today = date.today()

    try:
        records = sheets_service.get_all()
    except Exception as e:
        logger.exception("Не удалось прочитать Google Sheets: %s", e)
        return

    for row in records:
        name = row.get("Имя", "").strip()
        date_str = str(row.get("Дата рождения", "")).strip()
        if not name or not date_str:
            continue

        bd = parse_date(date_str)
        if not bd:
            continue

        diff = days_until_birthday(bd, today)

        if diff == 0:
            text = f"🎉 <b>Сегодня день рождения у {name}!</b>\nНе забудьте поздравить."
        elif diff == config.DAYS_BEFORE:
            text = (
                f"🔔 Через <b>{config.DAYS_BEFORE} дн.</b> день рождения у <b>{name}</b> "
                f"({bd.strftime('%d.%m')})."
            )
        else:
            continue

        try:
            await bot.send_message(config.ADMIN_CHAT_ID, text)
        except Exception as e:
            logger.exception("Не удалось отправить сообщение: %s", e)


def setup_scheduler(bot: Bot) -> None:
    scheduler.add_job(
        check_birthdays,
        CronTrigger(hour=config.REMINDER_HOUR, minute=config.REMINDER_MINUTE),
        args=[bot],
        id="daily_birthday_check",
        replace_existing=True,
    )
    scheduler.start()
    logger.info(
        "Планировщик запущен: ежедневно в %02d:%02d (%s)",
        config.REMINDER_HOUR,
        config.REMINDER_MINUTE,
        config.TIMEZONE,
    )
