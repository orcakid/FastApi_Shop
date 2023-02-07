from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeMeta, declarative_base, sessionmaker
from ..core.config import *



db_url = f'postgresql+asyncpg://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'
engine = create_async_engine(url=db_url, future=True)

async_session = sessionmaker(expire_on_commit=False, class_=AsyncSession, bind=engine)

Base: DeclarativeMeta = declarative_base()


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session