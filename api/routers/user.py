from fastapi import APIRouter, HTTPException

router = APIRouter(prefix='/user', tags=['User'])


@router.post('', status_code=201)
async def create_user():
    raise HTTPException(501)


@router.patch('/{id}')
async def update_user():
    raise HTTPException(501)


@router.delete('/{id}', status_code=204)
async def delete_user():
    raise HTTPException(501)


@router.get('')
async def list_user():
    raise HTTPException(501)


@router.get('/{id}')
async def get_user():
    raise HTTPException(501)


@router.post('/login')
async def login_user():
    raise HTTPException(501)
