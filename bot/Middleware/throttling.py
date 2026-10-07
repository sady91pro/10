import time
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User


class ThrottlingMiddleware(BaseMiddleware):
    """Простой антиспам: не чаще 1 сообщения в N секунд от одного пользователя."""

    def __init__(self, rate_limit: float = 0.5) -> None:
        self.rate_limit = rate_limit
        self._last_call: Dict[int, float] = {}

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user: User | None = data.get("event_from_user")
        if user is None:
            return await handler(event, data)

        now = time.monotonic()
        last = self._last_call.get(user.id, 0.0)
        if now - last < self.rate_limit:
            return None

        self._last_call[user.id] = now
        return await handler(event, data)
