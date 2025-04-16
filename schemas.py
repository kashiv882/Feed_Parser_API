from typing import List
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class ShowUser(BaseModel):
    id: int
    username: str

class UserClaims(BaseModel):
    sub: str
    permissions: List[str] = []
    roles: List[str] = [] 

class FeedSourceCreate(BaseModel):
    url: str
    heading: str
    domain: str

class FeedInput(BaseModel):
    url: str
    heading: str

    class Config:
        orm_mode = True
