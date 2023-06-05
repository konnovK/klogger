import asyncio
import uuid
from fastapi import APIRouter, Depends, HTTPException
from api.utils.telegram import multicast_log_item

from db import DB

from api.dependencies import get_db, check_auth
from api.schemas.log_item import CreateLogItemRequest, LogItemResponse, ListLogItemResponse
from api.globals import log_item_controller

router = APIRouter(prefix='/log', tags=['LogItem'])


@router.post('', status_code=201)
async def create_log_item(body: CreateLogItemRequest, log_group_id: uuid.UUID, db: DB = Depends(get_db), user_id: str = Depends(check_auth)) -> LogItemResponse:
    created_log_item = await log_item_controller.create_log_item(db, body.level, body.message, body.timestamp, log_group_id, user_id)
    if created_log_item is None:
        raise HTTPException(400, 'wrong request data')
    try:
        task = asyncio.create_task(multicast_log_item(body.level, body.timestamp, body.message))
    except Exception:
        pass
    return LogItemResponse(**created_log_item.dict())


@router.delete('/{id}', status_code=204)
async def delete_log_item(id: uuid.UUID, db: DB = Depends(get_db), user_id: str = Depends(check_auth)):
    deleted_log_item_id = await log_item_controller.delete_log_item_by_id_and_user_id(db, id, user_id)
    if deleted_log_item_id is None:
        raise HTTPException(400, "cannot delete this LogItem")
    return {}


@router.get('')
async def list_log_items(
    log_group_id: uuid.UUID,
    level: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
    db: DB = Depends(get_db),
    user_id: str = Depends(check_auth)
) -> ListLogItemResponse:
    log_items = await log_item_controller.get_log_items(db, log_group_id, user_id, level, limit, offset)
    if log_items is None:
        raise HTTPException(400, "wrong request data")
    log_items_count = await log_item_controller.get_log_items_count(db, log_group_id, user_id, level)
    if log_items_count is None:
        raise HTTPException(400, "wrong request data")
    return ListLogItemResponse(count=log_items_count, items=[LogItemResponse(**log_item.dict()) for log_item in log_items])
