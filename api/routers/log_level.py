from fastapi import APIRouter, HTTPException, Depends
from loguru import logger

from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError

from api.dependencies import get_db
from api.globals import log_levels
from api.schemas.log_level import CreateLogLevelRequest, LogLevelResponse

from db import DB, LogLevel

router = APIRouter(prefix='/log-level', tags=['LogLevel'])


@router.post('', status_code=201)
async def create_log_level(body: CreateLogLevelRequest, db: DB = Depends(get_db)) -> LogLevelResponse:
    async with db.async_session() as session:
        session: AsyncSession
        try:
            log_level = LogLevel(name=body.name)
            session.add(log_level)
            await session.commit()
            await session.refresh(log_level)
            return log_level
        except IntegrityError:
            logger.info(f'TRY TO CREATE LogLevel {body.name}, THATS ALREADY EXISTS')
            raise HTTPException(409, f"{body.name} is already exists")


@router.delete('/{name}', status_code=204)
async def delete_log_level(name: log_levels, db: DB = Depends(get_db)):
    async with db.async_session() as session:
        session: AsyncSession
        log_level = await session.scalar(sa.select(LogLevel).where(LogLevel.name == name))
        if log_level is None:
            raise HTTPException(400, f"{name} is not exists")
        await session.delete(log_level)
        await session.commit()
        return {}


@router.get('')
async def list_log_levels(db: DB = Depends(get_db)) -> list[LogLevelResponse]:
    async with db.async_session() as session:
        session: AsyncSession
        log_levels = (await session.execute(sa.select(LogLevel))).scalars().all()
        return log_levels
