from fastapi import APIRouter, Depends
from ..service.service import UserCrud
from ..models.schemas import CreateUSer, UserRead, DeleteUSer

router = APIRouter()


@router.get('/users', response_model=list[UserRead], tags=['Users'])
async def get_users(service: UserCrud = Depends()):
    return await service.get_all_users()


@router.post('/user/create', tags=['Users'])
async def create_new_us(us: CreateUSer, service: UserCrud = Depends()):
    return await service.create_user(us=us)


@router.delete('/user/delete_user', tags=['Users'])
async def delete_user(us: DeleteUSer, service: UserCrud = Depends()):
    return await service.delete_user(us=us)