from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

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

class GoogleUser(BaseModel):
    iss: str
    firstname: str
    lastname: str
    picture: str
    email: EmailStr
    email_verified: bool
    sub: str
