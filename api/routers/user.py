import uuid
from fastapi import APIRouter, Depends, HTTPException
from loguru import logger

from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError

from api.dependencies import get_db
from api.schemas.user import CreateUserRequest, LoginRequest, LoginResponse, UserResponse
from api.utils import hash_password
from api.utils import create_jwt

from db import DB, User

router = APIRouter(prefix='/user', tags=['User'])


@router.post('', status_code=201)
async def create_user(body: CreateUserRequest, db: DB = Depends(get_db)) -> UserResponse:
    async with db.async_session() as session:
        session: AsyncSession
        password_hash = hash_password(body.email, body.password)
        try:
            user_db = User(email=body.email, password_hash=password_hash)
            session.add(user_db)
            await session.commit()
            await session.refresh(user_db)
            return user_db
        except IntegrityError:
            logger.debug(f"TRY TO CREATE User {body.email}, THATS ALREADY EXISTS")
            raise HTTPException(409, f"User with email {body.email} is already exists")


@router.patch('/{id}', deprecated=True)
async def update_user(id: uuid.UUID) -> UserResponse:
    raise HTTPException(501)


@router.delete('/{id}', status_code=204)
async def delete_user(id: uuid.UUID, db: DB = Depends(get_db)):
    async with db.async_session() as session:
        session: AsyncSession
        user_db = await session.scalar(sa.select(User).where(User.id == id))
        if user_db is None:
            raise HTTPException(400, f"User with id {id} is not exists")
        await session.delete(user_db)
        await session.commit()
        return {}


@router.get('')
async def list_users(db: DB = Depends(get_db)) -> list[UserResponse]:
    async with db.async_session() as session:
        session: AsyncSession
        users_db = (await session.execute(sa.select(User))).scalars().all()
        return users_db


@router.get('/{id}')
async def get_user(id: uuid.UUID, db: DB = Depends(get_db)) -> UserResponse:
    async with db.async_session() as session:
        session: AsyncSession
        user_db = await session.scalar(sa.select(User).where(User.id == id))
        if user_db is None:
            raise HTTPException(400, f"User with id {id} is not exists")
        return user_db


@router.post('/login')
async def login_user(body: LoginRequest, db: DB = Depends(get_db)) -> LoginResponse:
    async with db.async_session() as session:
        session: AsyncSession
        password_hash = hash_password(body.email, body.password)
        user_db = await session.scalar(sa.select(User).where(User.email == body.email).where(User.password_hash == password_hash))
        if user_db is None:
            raise HTTPException(400, f"User with id {id} is not exists")
        try:
            access_token, refresh_token, expires_in = create_jwt(str(user_db.id))
        except Exception as err:
            logger.error(err)
            raise HTTPException(400, f"Bad request data for create token")
        return LoginResponse(access_token=access_token, refresh_token=refresh_token, access_token_expires_in=expires_in)
