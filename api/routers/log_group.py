from fastapi import APIRouter, Depends, HTTPException, Query
from loguru import logger

from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError

from api.dependencies import get_db, check_auth
from api.schemas.log_group import LogGroupResponse, CreateLogGroupRequest

from db import DB, User, LogGroup


router = APIRouter(prefix='/log-group', tags=['LogGroup'])


@router.post('', status_code=201)
async def create_log_group(body: CreateLogGroupRequest, db: DB = Depends(get_db), user_id: str = Depends(check_auth)) -> LogGroupResponse:
    async with db.async_session() as session:
        session: AsyncSession
        user_db = await session.scalar(sa.select(User).where(User.id == user_id))
        if user_db is None:
            raise HTTPException(401, "wrong access token")
        try:
            log_group = LogGroup(name=body.name, description=body.description, user=user_db)
            session.add(log_group)
            await session.commit()
            await session.refresh(log_group)
            return log_group
        except IntegrityError:
            raise HTTPException(409, f'LogGroup {body.name} is already exists')



@router.patch('/{id}', deprecated=True)
async def update_log_group():
    raise HTTPException(501)


@router.delete('/{id}', status_code=204)
async def delete_log_group(id: str, db: DB = Depends(get_db), user_id: str = Depends(check_auth)):
    async with db.async_session() as session:
        session: AsyncSession
        user_db = await session.scalar(sa.select(User).where(User.id == user_id))
        if user_db is None:
            raise HTTPException(401, "wrong access token")
        log_group = await session.scalar(sa.select(LogGroup).where(LogGroup.id == id))
        if log_group is None:
            raise HTTPException(409, f'LogGroup with id={id} is not exists')
        if str(log_group.user_id) != user_id:
            raise HTTPException(403, f'you have no permissions for deleting this LogGroup')
        await session.delete(log_group)
        await session.commit()
        return {}


@router.get('')
async def list_log_groups(user_email: str | None = None, db: DB = Depends(get_db)):
    async with db.async_session() as session:
        session: AsyncSession
        if user_email is None or user_email == '':
            log_groups = (await session.execute(sa.select(LogGroup))).scalars().all()
            return log_groups
        else:
            stmt = sa.select(LogGroup).where(User.email == user_email)
            log_groups = (await session.execute(stmt)).scalars().all()
            return log_groups
