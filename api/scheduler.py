import datetime
from rocketry import Rocketry
from loguru import logger

from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa

from db import LogItem

from api.globals import settings, db

scheduler = Rocketry()
log_item_ttl = datetime.timedelta(seconds=settings.log_item_ttl)


async def _delete_old_log_items():
    logger.debug(f"DELETE OLD LOG ITEMS: TTL OF LogItem == {log_item_ttl}")
    async with db.async_session() as session:
        session: AsyncSession
        count = (await session.execute(sa.delete(LogItem).where(LogItem.timestamp < datetime.datetime.now() - log_item_ttl).returning(LogItem.id))).scalars().all()
        await session.commit()
        logger.debug(f"DELETE OLD LOG ITEMS: DELETE {len(count)} LogItems")



@scheduler.task('daily')
async def schedule_delete_old_log_items():
    await _delete_old_log_items()
