import datetime
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa

from controllers.schemas.log_item import LogItemResponse
from db import DB, LogItem, LogGroup, LogLevel


class LogItemController:
    @staticmethod
    async def create_log_item(db: DB, level: str, message: str, timestamp: datetime.datetime, log_group_id: uuid.UUID, user_id: uuid.UUID) -> LogItemResponse | None:
        async with db.async_session() as session:
            session: AsyncSession
            log_group_db_id = await session.scalar(sa.select(LogGroup.id).where(LogGroup.user_id == user_id).where(LogGroup.id == log_group_id))
            if log_group_db_id is None:
                return None
            log_level_db_name = await session.scalar(sa.select(LogLevel.name).where(LogLevel.name == level))
            if log_level_db_name is None:
                return None

            log_item = LogItem(log_level_name=log_level_db_name, log_group_id=log_group_db_id, message=message, timestamp=timestamp)
            session.add(log_item)
            await session.commit()
            await session.refresh(log_item)
        return LogItemResponse.from_orm(log_item)

    @staticmethod
    async def delete_log_item_by_id_and_user_id(db: DB, id: uuid.UUID, user_id: uuid.UUID) -> uuid.UUID | None:
        async with db.async_session() as session:
            session: AsyncSession
            stmt = sa.delete(LogItem).where(LogItem.id == id).where(LogGroup.user_id == user_id).returning(LogItem.id)
            deleted_log_item_id = await session.scalar(stmt)
            await session.commit()
        return deleted_log_item_id

    @staticmethod
    async def get_log_items(
        db: DB, log_group_id: uuid.UUID,
        user_id: uuid.UUID,
        level: str | None,
        limit: int | None = None,
        offset: int | None = None
    ) -> list[LogItemResponse] | None:
        async with db.async_session() as session:
            session: AsyncSession
            log_group_db_id = await session.scalar(sa.select(LogGroup.id).where(LogGroup.id == log_group_id).where(LogGroup.user_id == user_id))
            if log_group_db_id is None:
                return None

            stmt = sa.select(LogItem).where(LogItem.log_group_id == log_group_db_id)

            if level is not None:
                level_name = await session.scalar(sa.select(LogLevel.name).where(LogLevel.name == level))
                if level_name is None:
                    return None
                stmt = stmt.where(LogItem.log_level_name == level_name)
            if limit is not None:
                stmt = stmt.limit(limit)
            if offset is not None:
                stmt = stmt.offset(offset)

            log_items = (await session.execute(stmt)).scalars().all()

            return [LogItemResponse.from_orm(log_item) for log_item in log_items]

    @staticmethod
    async def get_log_items_count(
        db: DB, log_group_id: uuid.UUID,
        user_id: uuid.UUID,
        level: str | None
    ) -> int | None:
        async with db.async_session() as session:
            session: AsyncSession
            log_group_db_id = await session.scalar(sa.select(LogGroup.id).where(LogGroup.id == log_group_id).where(LogGroup.user_id == user_id))
            if log_group_db_id is None:
                return None

            stmt = sa.select(sa.func.count()).select_from(LogItem).where(LogItem.log_group_id == log_group_db_id)

            if level is not None:
                level_name = await session.scalar(sa.select(LogLevel.name).where(LogLevel.name == level))
                if level_name is None:
                    return None
                stmt = stmt.where(LogItem.log_level_name == level_name)

            count = await session.scalar(stmt)

            return count
