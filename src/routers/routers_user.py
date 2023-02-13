from fastapi import APIRouter, Depends
from ..service.service_user import UserCrud
from ..schemas.schemas_user import CreateUSer, USerUpdate, DeleteUSer, UserLogin
from fastapi.security import OAuth2PasswordRequestForm
from ..auth.deps import get_current_user

router = APIRouter()


@router.post('/login', tags=['login'])
async def login(form_data: OAuth2PasswordRequestForm = Depends(), service: UserCrud = Depends()):
    return await service.login(form_data)


@router.post('/signup', tags=['Users'], summary='Create a new user')
async def new_user(user: CreateUSer, service: UserCrud = Depends()):
    return await service.new_user(user)
    

@router.get('/users', tags=['Users'], summary='Only for admin')
async def get_users(service: UserCrud = Depends(), user: str = Depends(get_current_user)):
    if user.email == "admin@mail.com":
        return await service.get_all_users()
    
    return {'message':"You don't have access"}


@router.delete('/user/delete_user', tags=['Users'], summary='Only for admin')
async def delete_user(us: DeleteUSer, service: UserCrud = Depends(), user: str = Depends(get_current_user)):
    if user.email == "admin@mail.com":
        return await service.delete_user(us=us)
    return {'message':"You don't have access"}


@router.patch('/update', tags=['Users'], summary='Update your')
async def update_user(user: USerUpdate, service: UserCrud = Depends(), us: str = Depends(get_current_user)):
    return await service.update_user(us=user, email=us.email)



    
    
