from typing import Callable, Awaitable, Any, cast
from aiogram.types import TelegramObject, Update
from aiogram import BaseMiddleware
from asyncpg import Pool


class DbSessionMiddleware(BaseMiddleware):
    def __init__(self, db_pool: Pool):
        super().__init__()
        self.db_pool = db_pool

    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: dict[str, Any],
    ) -> Any:

        event = cast(Update, event)
        await handler(event, data)
        return
