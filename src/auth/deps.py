from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from ..auth.auth import (
    ALGORITHM,
    JWT_SECRET_KEY
)
from ..db.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt
from pydantic import ValidationError
from sqlalchemy import select
from ..models.model_user import User

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)



async def get_current_user(token: str = Depends(reuseable_oauth), ses: AsyncSession = Depends(get_async_session)):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        token_data = payload
        
        if datetime.fromtimestamp(token_data['exp']) < datetime.now():
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    q = select(User).where(User.email == token_data['sub'])
    res = await ses.execute(q)
    user = res.scalar_one_or_none()
    if user is None:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Could not find user",
        )
        
    return user
    


