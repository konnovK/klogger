import uuid
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa

from controllers.schemas.log_group import LogGroupResponse
from db import DB, LogGroup


class LogGroupController:
    @staticmethod
    async def create_log_group(db: DB, user_id: uuid.UUID, name: str, description: str | None) -> LogGroupResponse:
        async with db.async_session() as session:
            session: AsyncSession
            log_group = LogGroup(name=name, description=description, user_id=user_id)
            session.add(log_group)
            await session.commit()
            await session.refresh(log_group, ['id', 'created_at', 'name', 'description'])
        return LogGroupResponse.from_orm(log_group)

    @staticmethod
    async def delete_log_group_by_id_and_user_id(db: DB, log_group_id: uuid.UUID, user_id: uuid.UUID):
        async with db.async_session() as session:
            session: AsyncSession
            stmt = sa.delete(LogGroup).where(LogGroup.id == log_group_id).where(LogGroup.user_id == user_id).returning(LogGroup.id)
            deleted_log_group_id = await session.scalar(stmt)
            await session.commit()
        return deleted_log_group_id

    @staticmethod
    async def get_list_log_groups(db: DB, user_id: uuid.UUID | None) -> list[LogGroupResponse]:
        async with db.async_session() as session:
            session: AsyncSession
            stmt = sa.select(LogGroup.id, LogGroup.created_at, LogGroup.name, LogGroup.description)
            if user_id is not None:
                stmt = stmt.where(LogGroup.user_id == user_id)
            log_groups = (await session.execute(stmt)).all()
        return [
            LogGroupResponse(
                id=log_group[0],
                created_at=log_group[1],
                name=log_group[2],
                description=log_group[3]
            )
            for log_group in log_groups
        ]
