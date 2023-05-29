from fastapi import APIRouter, HTTPException, Depends
from loguru import logger

from sqlalchemy.exc import IntegrityError

from api.dependencies import get_db, check_auth
from api.schemas.log_level import CreateLogLevelRequest, LogLevelResponse
from api.globals import log_level_controller

from db import DB

router = APIRouter(prefix='/log-level', tags=['LogLevel'])


@router.post('', status_code=201)
async def create_log_level(body: CreateLogLevelRequest, db: DB = Depends(get_db), user_id: str = Depends(check_auth)) -> LogLevelResponse:
    logger.debug(f'USER WITH id={user_id} TRY TO CREATE LogLevel {body.name}')
    try:
        log_level = await log_level_controller.create_log_level(db, body.name)
        return LogLevelResponse(**log_level.dict())
    except IntegrityError:
        logger.debug(f'TRY TO CREATE LogLevel {body.name}, THATS ALREADY EXISTS')
        raise HTTPException(409, f"{body.name} is already exists")


@router.delete('/{name}', status_code=204)
async def delete_log_level(name: str, db: DB = Depends(get_db), user_id: str = Depends(check_auth)):
    logger.debug(f'USER WITH id={user_id} TRY TO DELETE LogLevel {name}')
    deleted_log_level_name = await log_level_controller.delete_log_level_by_name(db, name)
    if deleted_log_level_name is None:
        raise HTTPException(400, f"{name} is not exists")
    return {}


@router.get('')
async def list_log_levels(db: DB = Depends(get_db)) -> list[LogLevelResponse]:
    log_levels = await log_level_controller.get_all_log_levels(db)
    return [LogLevelResponse(**log_level.dict()) for log_level in log_levels]
