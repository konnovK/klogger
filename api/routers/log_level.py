from fastapi import APIRouter, HTTPException

router = APIRouter(prefix='/log-level', tags=['LogLevel'])


@router.post('', status_code=201)
async def create_log_level():
    raise HTTPException(501)


@router.delete('/{name}', status_code=204)
async def delete_log_level():
    raise HTTPException(501)


@router.get('')
async def list_log_level():
    raise HTTPException(501)
