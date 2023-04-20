from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware, types
from aiogram.dispatcher.flags import get_flag
from aiogram.utils.chat_action import ChatActionSender

class MyMiddelware(BaseMiddleware):
    
    async def __call__(
            self,
            handler: Callable[[types.TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: types.Message,
            data: Dict[str, Any],
    ) -> Any:
        long_operation = get_flag(handler=data, name='long_operation')

        if long_operation:
            async with ChatActionSender(action=long_operation, chat_id=event.chat.id):
                return await handler(event, data)
        return await handler(event, data)
