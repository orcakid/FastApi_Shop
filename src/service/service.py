from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from ..db.database import get_async_session
from ..models.schemas import UserRead , CreateUSer, DeleteUSer
from ..models.model import User
from sqlalchemy import select, insert



class UserCrud:
    def __init__(self, session: AsyncSession = Depends(get_async_session)) -> None:
        self.session = session
        
    async def get_all_users(self) -> list[UserRead]:
        q = select(User)
        res = await self.session.execute(q)
        users = res.scalars().all()
        return users


    async def create_user(self, us: CreateUSer) -> UserRead:
        stmt = insert(User).values(**us.dict())
        await self.session.execute(stmt)
        try:
            await self.session.commit()
            return {'user': 'added'}
        except Exception:
            await self.session.rollback()
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        
    async def delete_user(self, us: DeleteUSer):
        q = select(User).where(User.email == us.email).where(User.hashed_password == us.hashed_password)
        result = await self.session.execute(q)
        delete_user = result.scalar_one_or_none()
        if delete_user is None:
            # потом улучшичть чтобы проверялось наличие и пароля и емейла
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='wrong email or password')
        else:
            await self.session.delete(delete_user)
            await self.session.commit()
            return {"user": "has been deleted"}