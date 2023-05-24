from fastapi import APIRouter, HTTPException

router = APIRouter(prefix='/log', tags=['LogItem'])


@router.post('', status_code=201)
async def create_log_item():
    raise HTTPException(501)


@router.delete('', status_code=204)
async def delete_log_item():
    raise HTTPException(501)


@router.get('')
async def list_log_item():
    raise HTTPException(501)
