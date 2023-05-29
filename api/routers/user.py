import uuid
from fastapi import APIRouter, Depends, HTTPException
from loguru import logger

from sqlalchemy.exc import IntegrityError

from db import DB

from api.dependencies import check_auth, get_db
from api.schemas.user import CreateUserRequest, LoginRequest, LoginResponse, UserResponse
from api.utils import create_jwt
from api.globals import user_controller


router = APIRouter(prefix='/user', tags=['User'])


@router.post('', status_code=201)
async def create_user(body: CreateUserRequest, db: DB = Depends(get_db)) -> UserResponse:
    try:
        user = await user_controller.create_user(db, body.email, body.password)
        return UserResponse(**user.dict())
    except IntegrityError:
        logger.debug(f"TRY TO CREATE User {body.email}, THATS ALREADY EXISTS")
        raise HTTPException(409, f"User with email {body.email} is already exists")


@router.patch('/{id}', deprecated=True)
async def update_user(id: uuid.UUID) -> UserResponse:
    raise HTTPException(501)


@router.delete('/{id}', status_code=204)
async def delete_user(id: uuid.UUID, db: DB = Depends(get_db), user_id: str = Depends(check_auth)):
    if user_id != str(id):
        raise HTTPException(403, 'you cannot delete this user')
    deleted_user_id = await user_controller.delete_user_by_id(db, id)
    if deleted_user_id is None:
        raise HTTPException(400, f"User with id {id} is not exists")
    return {}


@router.get('')
async def list_users(db: DB = Depends(get_db)) -> list[UserResponse]:
    users = await user_controller.get_list_users(db)
    return [UserResponse(**user.dict()) for user in users]


@router.get('/{id}')
async def get_user(id: uuid.UUID, db: DB = Depends(get_db)) -> UserResponse:
    user = await user_controller.get_user_by_id(db, id)
    if user is None:
        raise HTTPException(400, f"User with id {id} is not exists")
    return UserResponse(**user.dict())


@router.post('/login')
async def login_user(body: LoginRequest, db: DB = Depends(get_db)) -> LoginResponse:
    user_id = await user_controller.get_user_id_by_email_and_password(db, body.email, body.password)
    if user_id is None:
            raise HTTPException(400, f"User with id {user_id} is not exists")
    try:
        access_token, refresh_token, expires_in = create_jwt(str(user_id))
    except Exception as err:
        logger.debug(err)
        raise HTTPException(400, f"Bad request data for create token")
    return LoginResponse(access_token=access_token, refresh_token=refresh_token, access_token_expires_in=expires_in)
