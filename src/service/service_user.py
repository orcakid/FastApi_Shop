from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from ..db.database import get_async_session
from ..schemas.schemas_user import BaseUser , CreateUSer, DeleteUSer, UserLogin
from ..schemas.token_schemas import Token
from ..models.model_user import User
from sqlalchemy import select, insert
from ..auth.auth import get_hash_pwd, create_access_token, verify_password, create_refresh_token
from fastapi.security import OAuth2PasswordRequestForm



class UserCrud:
    def __init__(self, session: AsyncSession = Depends(get_async_session)) -> None:
        self.session = session
        
    
    async def login(self, form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
        q = select(User).where(User.username == form_data.username)
        res = await self.session.execute(q)
        user = res.scalar_one_or_none()
        if user is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='invalid username')
        hash_pass = user.hashed_password
        if not verify_password(form_data.password, hash_pass):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='invalid password')
        
        return {
            'access_token': create_access_token(user.email),
            'refresh_token': create_refresh_token(user.email)
        }
    
    
    async def new_user(self, user: CreateUSer):
        res = await self.session.execute(select(User).where(User.email == user.email))
        user_db = res.scalar_one_or_none()
        if user_db:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        pass_hash = get_hash_pwd(user.hashed_password)
        new_user = insert(User).values(username=user.username, email=user.email, hashed_password=pass_hash)
        await self.session.execute(new_user)
        try:
            await self.session.commit()
            return {'user': 'added'}
        except Exception:
            await self.session.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        
        
    async def get_all_users(self) -> list[BaseUser]:
        q = select(User)
        res = await self.session.execute(q)
        users = res.scalars().all()
        return users


    async def update_user(self, us: CreateUSer, email: str) -> BaseUser:
        #stmt = insert(User).values(**us.dict())
        q = select(User).where(User.email == email)
        res = await self.session.execute(q)
        user_update = res.scalar_one_or_none()
        try:
            user_update.username = us.username
            await self.session.commit()
            return {'user': 'updated'}
        except Exception:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        
    async def delete_user(self, us: DeleteUSer):
        q = select(User).where(User.email == us.email)
        result = await self.session.execute(q)
        delete_user = result.scalar_one_or_none()
        if delete_user is None:
            # потом улучшичть чтобы проверялось наличие и пароля и емейла
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='wrong email or password')
        else:
            await self.session.delete(delete_user)
            await self.session.commit()
            return {"user": "has been deleted"}
        
    async def login_user(self, us: UserLogin):
        q = select(User).where(User.username == us.username).where(User.hashed_password == us.hashed_password)
        res = await self.session.execute(q)
        user = res.scalar_one_or_none()
        if user is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='user not exist')
        else:
            return user
        