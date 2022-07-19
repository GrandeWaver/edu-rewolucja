from lib2to3.pgen2 import token
from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class Post(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime

class PostDetails(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    class_id: int
    # comments
    # files
    # etc

class UserCreate(BaseModel):
    email: EmailStr
    firstname: str
    lastname: str
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    firstname: str
    lastname: str
    picture: str
    created_at: datetime
    account_type: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
    account_type: Optional[str] = None

class Email(BaseModel):
    email: EmailStr

class GoogleToken(BaseModel):
    token: str

class Schedule(BaseModel):
    day: str
    hour: int

class Class(BaseModel):
    id: int
    subject: str
    firstname: str
    lastname: str

class ClassDetails(BaseModel):
    subject: str
    # firstname
    # lastname
    # homework