import email
from typing import List, Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
# from .models import User

class ArticleBase(BaseModel):
    title:str
    body: Optional[str]=None
    
class ArticleCreate(ArticleBase):
    pass

class UserBase(BaseModel):
    email:EmailStr

class UserForArtical(UserBase):
    id:int
    is_active:bool

    class Config:
        orm_mode = True


class Article(ArticleBase):
    id:int
    author:UserForArtical
    created_at:datetime
    updated_at:Optional[datetime]

    class Config:
        orm_mode = True

class ArticleUpdate(BaseModel):
    title:Optional[str]
    body: Optional[str]

    class Config:
        orm_mode=True



class UserCreate(UserBase):
    password:str

class User(UserBase):
    id:int
    is_active:bool
    articles:List[Article]=[]

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token : str
    token_type : str


class TokenData(BaseModel):
    username:str|None = None