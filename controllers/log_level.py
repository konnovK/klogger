from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa

from controllers.schemas.log_level import LogLevelResponse
from db import DB, LogLevel


class LogLevelController:
    @staticmethod
    async def create_log_level(db: DB, name: str) -> LogLevelResponse:
        async with db.async_session() as session:
            session: AsyncSession
            log_level = LogLevel(name=name)
            session.add(log_level)
            await session.commit()
            await session.refresh(log_level, ['name', 'created_at'])
        return LogLevelResponse.from_orm(log_level)

    @staticmethod
    async def delete_log_level_by_name(db: DB, name: str) -> str | None:
        async with db.async_session() as session:
            session: AsyncSession
            deleted_log_level_name = await session.scalar(sa.delete(LogLevel).where(LogLevel.name == name).returning(LogLevel.name))
            await session.commit()
        return deleted_log_level_name

    @staticmethod
    async def get_all_log_levels(db: DB) -> list[LogLevelResponse]:
        async with db.async_session() as session:
            session: AsyncSession
            stmt = sa.select(LogLevel.name, LogLevel.created_at)
            log_levels = (await session.execute(stmt)).all()
        return [LogLevelResponse(name=log_level[0], created_at=log_level[1]) for log_level in log_levels]
