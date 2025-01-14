import logging
from typing import Callable, Awaitable, Any

from aiogram import BaseMiddleware
from aiogram.types import Update

from db import User

class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any]
    ) -> Any:
        current_event = (
            event.message or
            event.callback_query or
            event.pre_checkout_query
        )
        if not current_event:
            return await handler(event, data)
        #logging.warn(f"@{current_event.from_user.username} triggered event.")

        user = await User.get_or_create(
            id=current_event.from_user.id,
            defaults={
                "username": current_event.from_user.username,
                "stars": 0
            }
        )

        data["user"] = user[0]
        return await handler(event, data)