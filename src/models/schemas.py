from pydantic import BaseModel


class UserRead(BaseModel):
    id: int | None
    username: str
    email: str
    
    class Config:
        orm_mode = True
    
class CreateUSer(BaseModel):
    username: str
    email: str
    hashed_password: str
    
    class Config:
        orm_mode = True
        
class DeleteUSer(BaseModel):
    email: str
    hashed_password: str
    
    class Config:
        orm_mode = True