import uuid
from fastapi import APIRouter, Depends, HTTPException
from loguru import logger

from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError

from api.dependencies import get_db, check_auth
from api.schemas.log_item import CreateLogItemRequest, LogItemResponse
from api.globals import log_levels

from db import DB, User, LogGroup, LogItem, LogLevel

router = APIRouter(prefix='/log', tags=['LogItem'])


@router.post('', status_code=201)
async def create_log_item(body: CreateLogItemRequest, log_group_id: uuid.UUID, db: DB = Depends(get_db), user_id: str = Depends(check_auth)) -> LogItemResponse:
    async with db.async_session() as session:
        session: AsyncSession
        user_db = await session.scalar(sa.select(User).where(User.id == user_id))
        if user_db is None:
            raise HTTPException(401, "wrond access token")
        log_group = await session.scalar(sa.select(LogGroup).where(LogGroup.id == log_group_id).where(User.id == user_id))
        if log_group is None:
            raise HTTPException(403, "you cannot write logs to this group")
        log_level = await session.scalar(sa.select(LogLevel).where(LogLevel.name == body.level))
        if log_level is None:
            raise HTTPException(400, 'wrong log level')

        log_item = LogItem(log_level=log_level, log_group=log_group, message=body.message, timestamp=body.timestamp)

        session.add(log_item)

        await session.commit()
        await session.refresh(log_item)

        return log_item


@router.delete('/{id}', status_code=204)
async def delete_log_item(id: uuid.UUID, db: DB = Depends(get_db), user_id: str = Depends(check_auth)):
    async with db.async_session() as session:
        session: AsyncSession
        user_db = await session.scalar(sa.select(User).where(User.id == user_id))
        if user_db is None:
            raise HTTPException(401, "wrond access token")
        log_item = await session.scalar(sa.select(LogItem, LogGroup).where(LogItem.id == id).where(User.id == user_id))
        logger.debug(log_item)
        if log_item is None:
            raise HTTPException(400, "wrond LogItem id")
        await session.delete(log_item)
        await session.commit()
        return {}


@router.get('')
async def list_log_items(
    log_group_id: uuid.UUID,
    level: log_levels | None = None,
    limit: int | None = None,
    offset: int | None = None,
    db: DB = Depends(get_db),
    user_id: str = Depends(check_auth)
) -> list[LogItemResponse]:
    async with db.async_session() as session:
        session: AsyncSession
        user_db = await session.scalar(sa.select(User).where(User.id == user_id))
        if user_db is None:
            raise HTTPException(401, "wrond access token")
        log_group = await session.scalar(sa.select(LogGroup).where(User.id == user_id))
        if log_group is None:
            raise HTTPException(403, "you cannot read logs from this group")
        
        stmt = sa.select(LogItem).where(LogGroup.id == log_group_id)

        if level is not None:
            stmt = stmt.where(LogLevel.name == level)
        if limit is not None:
            stmt = stmt.limit(limit)
        if offset is not None:
            stmt = stmt.offset(offset)

        log_items = (await session.execute(stmt)).scalars().all()
        return log_items
