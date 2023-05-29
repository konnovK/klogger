from fastapi import Header, HTTPException, Depends
from fastapi.security import HTTPBearer
from loguru import logger
from api.globals import db, user_controller
from api.utils import check_access_token_unexpired, get_id_from_access_token
from db import DB


def get_db() -> DB:
    yield db


security = HTTPBearer()


async def check_auth(authorization = Depends(security)) -> str:
    if authorization is None:
        raise HTTPException(401, 'no access token')
    scheme = authorization.scheme
    token = authorization.credentials

    if scheme != 'Bearer':
        raise HTTPException(401, 'wrong access token scheme')
    if token is None:
        raise HTTPException(401, 'no access token')
    try:
        unexpired = check_access_token_unexpired(token)
    except Exception:
        raise HTTPException(401, 'wrong access token format')
    if not unexpired:
        raise HTTPException(401, 'expired access token')
    try:
        user_id = get_id_from_access_token(token)
    except Exception:
        raise HTTPException(401, 'wrong access token')
    if not (await user_controller.exists(db, user_id)):
        raise HTTPException(401, 'wrong access token')
    return user_id


all = [
    get_db,
    check_auth,
]
