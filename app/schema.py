from pydantic import BaseModel,ValidationError,EmailStr
from pydantic.types import conint
from sqlalchemy.sql.expression import true
from datetime import datetime
from typing import Union, Optional


class PostBase(BaseModel):
    title : str
    content : str
    published : bool = True

class UserOut(BaseModel):
    id : int
    created_at : datetime
    email : EmailStr

    class Config:
        orm_mode = True  
        
# vote model
class Vote(BaseModel):
    post_id : int
    dir : conint(le=1)
    
    class Config:
        orm_mode = True        

class CreatePost(PostBase):
    pass

class Post(PostBase):
    id : int
    created_at : datetime
    owner_id : int
    owner : UserOut
    
    class Config:
        orm_mode = True    

class PostOut(BaseModel):
    Post : Post
    votes : int

    class Config:
        orm_mode = True 

# users model
class UserBase(BaseModel):
    email : EmailStr
    password : str


class CreateUser(UserBase):
    pass

class UserLogin(BaseModel):
    email : EmailStr
    password : str

  

class Token(BaseModel):
    access_token : str
    token_type : str


class TokenData(BaseModel):
    id : Optional[str]





class CreateUser(UserBase):
    pass