from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from pydantic.networks import EmailStr


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    class Config:
        orm_mode = True

class User(BaseModel):
    email: EmailStr
    password: str
    class Config:
        orm_mode = True
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

