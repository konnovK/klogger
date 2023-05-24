from loguru import logger
from db import LogLevel
from api.globals import db

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError


async def create_log_level(name: str) -> LogLevel | None:
    async with db.async_session() as session:
        session: AsyncSession 
        try:
            log_level = LogLevel(name=name)
            session.add(log_level)
            await session.commit()
            return log_level
        except IntegrityError as err:
            logger.error(f'CANNOT CREATE LogLevel: {name=}')
            logger.error(err)
            return None


async def create_all_log_levels():
    log_level_names = [
        'DEBUG',
        'INFO',
        'WARNING',
        'ERROR',
        'CRITICAL'
    ]
    for log_level_name in log_level_names:
        await create_log_level(log_level_name)
