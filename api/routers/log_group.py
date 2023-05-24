from fastapi import APIRouter, HTTPException

router = APIRouter(prefix='/log-group', tags=['LogGroup'])


@router.post('', status_code=201)
async def create_log_group():
    raise HTTPException(501)


@router.patch('/{id}')
async def update_log_group():
    raise HTTPException(501)


@router.delete('/{id}', status_code=204)
async def delete_log_group():
    raise HTTPException(501)


@router.get('')
async def list_log_group():
    raise HTTPException(501)
