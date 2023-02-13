from fastapi import FastAPI
from .routers.routers_user import router

app = FastAPI()


app.include_router(router)