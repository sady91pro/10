import asyncio
import logging

from bot.bot import bot, dp
from bot.Handlers import register_all_handlers
from bot.Middleware.throttling import ThrottlingMiddleware
from bot.Services.scheduler import setup_scheduler


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    # Регистрация middleware
    dp.message.middleware(ThrottlingMiddleware(rate_limit=0.5))

    # Регистрация хендлеров
    register_all_handlers(dp)

    # Запуск планировщика напоминаний
    setup_scheduler(bot)

    logging.info("Бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен.")
