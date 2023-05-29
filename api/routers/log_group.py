import uuid
from fastapi import APIRouter, Depends, HTTPException
from loguru import logger

from sqlalchemy.exc import IntegrityError

from api.dependencies import get_db, check_auth
from api.schemas.log_group import LogGroupResponse, CreateLogGroupRequest
from api.globals import log_group_controller

from db import DB


router = APIRouter(prefix='/log-group', tags=['LogGroup'])


@router.post('', status_code=201)
async def create_log_group(body: CreateLogGroupRequest, db: DB = Depends(get_db), user_id: str = Depends(check_auth)) -> LogGroupResponse:
    logger.debug(f'USER WITH id={user_id} TRY TO CREATE LogGroup {body.name}')
    try:
        log_group = await log_group_controller.create_log_group(db, user_id, body.name, body.description)
        return LogGroupResponse(**log_group.dict())
    except IntegrityError:
        raise HTTPException(409, f'LogGroup {body.name} is already exists')


@router.patch('/{id}', deprecated=True)
async def update_log_group():
    raise HTTPException(501)


@router.delete('/{id}', status_code=204)
async def delete_log_group(id: uuid.UUID, db: DB = Depends(get_db), user_id: str = Depends(check_auth)):
    logger.debug(f'USER WITH id={user_id} TRY TO DELETE LogGroup {str(id)}')
    deleted_log_group_id = await log_group_controller.delete_log_group_by_id_and_user_id(db, id, user_id)
    if deleted_log_group_id is None:
        raise HTTPException(400, f'you cannot delete this LogGroup')
    return {}


@router.get('')
async def list_log_groups(db: DB = Depends(get_db), user_id: str = Depends(check_auth)) -> list[LogGroupResponse]:
    log_groups = await log_group_controller.get_list_log_groups(db, user_id)
    return [LogGroupResponse(**log_group.dict()) for log_group in log_groups]
