from hashlib import md5
import uuid

from controllers.schemas.user import UserResponse
from db import DB, User

from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa


class UserController:
    @staticmethod
    def _hash_password(email: str, password: str) -> str:
        return md5(f'{email}:{password}'.encode()).hexdigest()

    @staticmethod
    async def create_user(db: DB, email: str, password: str) -> UserResponse:
        async with db.async_session() as session:
            session: AsyncSession
            password_hash = UserController._hash_password(email, password)
            user_db = User(email=email, password_hash=password_hash)
            session.add(user_db)
            await session.commit()
            await session.refresh(user_db)
        return UserResponse.from_orm(user_db)

    @staticmethod
    async def delete_user_by_id(db: DB, user_id: uuid.UUID) -> uuid.UUID:
        async with db.async_session() as session:
            session: AsyncSession
            deleted_user_id = await session.scalar(sa.delete(User).where(User.id == user_id).returning(User.id))
            await session.commit()
        return deleted_user_id
    
    @staticmethod
    async def get_user_by_id(db: DB, user_id: uuid.UUID) -> UserResponse | None:
        async with db.async_session() as session:
            session: AsyncSession
            user_db = await session.scalar(sa.select(User).where(User.id == user_id))
            if user_db is None:
                return None
        return UserResponse.from_orm(user_db)

    @staticmethod
    async def get_list_users(db: DB, limit: int | None = None, offset: int | None = None) -> list[UserResponse]:
        async with db.async_session() as session:
            session: AsyncSession
            stmt = sa.select(User)
            if limit is not None:
                stmt = stmt.limit(limit)
            if offset is not None:
                stmt = stmt.offset(offset)
            users_db = (await session.execute(stmt)).scalars().all()
        return [UserResponse.from_orm(user_db) for user_db in users_db]

    @staticmethod
    async def get_user_id_by_email_and_password(db: DB, email: str, password: str) -> uuid.UUID | None:
        password_hash = UserController._hash_password(email, password)
        async with db.async_session() as session:
            session: AsyncSession
            user_id = await session.scalar(sa.select(User.id).where(User.email == email).where(User.password_hash == password_hash))
        return user_id

    @staticmethod
    async def exists(db: DB, id: uuid.UUID) -> bool:
        async with db.async_session() as session:
            session: AsyncSession
            user_id = await session.scalar(sa.select(User.id).where(User.id == id))
        return user_id is not None
