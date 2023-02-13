from pydantic import BaseModel


class BaseUser(BaseModel):
    username: str
    email: str
    
    class Config:
        orm_mode = True
        
class USerUpdate(BaseModel):
    username: str
    
    class Config:
        orm_mode = True
        
        
class CreateUSer(BaseUser):
    hashed_password: str
    
    class Config:
        orm_mode = True
        
class UserDB(BaseUser):
    id: int
    
    class Config:
        orm_mode = True
    
        
class DeleteUSer(BaseModel):
    email: str
    
    class Config:
        orm_mode = True
        
class UserLogin(BaseModel):
    username: str
    hashed_password: str
    
    class Config:
        schema_extra = {
            'example':
                {
                    'username': 'Joe Baiden',
                    'hashed_password': 'ViviCat2022'
                }
        }