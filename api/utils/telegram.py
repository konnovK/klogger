import datetime
from loguru import logger
import telegram
from api.globals import telegram_bot, settings


async def _multicast_message(bot: telegram.Bot, chat_ids: list[str], text: str):
    if settings.telegram_token is None or settings.telegram_users_ids is None:
        return
    for chat_id in chat_ids:
        logger.debug(f'TELEGRAM BOT: SEND MESSAGE {text=} {chat_id=}')
        await bot.send_message(text=text, chat_id=chat_id)


async def multicast_message(text: str):
    await _multicast_message(telegram_bot, settings.telegram_users_ids, text)


async def multicast_log_item(level: str, timestamp: datetime.datetime, message: str):
    if level.lower() not in settings.telegram_levels:
        return
    await multicast_message(f'{timestamp}\n{level}\n\n{message}')


__all__ = [
    multicast_log_item,
    multicast_message
]
