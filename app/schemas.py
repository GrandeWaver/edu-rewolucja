from calendar import day_name
from lib2to3.pgen2 import token
from typing import Optional, List
from pydantic import BaseModel, EmailStr
from datetime import datetime

class Post(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime

class NewPost(BaseModel):
    class_id: int
    title: str
    content: str

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
    picture: Optional[str] = None

class Email(BaseModel):
    email: EmailStr

class GoogleToken(BaseModel):
    token: str

class Schedule(BaseModel):
    day: str
    hour: str

class Class(BaseModel):
    id: int
    subject: str
    firstname: str
    lastname: str
    picture: str

class ClassV2(BaseModel):
    id: int
    subject: str
    firstname: str
    lastname: str
    picture: str
    schedules: List[Schedule]

class ClassDetails(BaseModel):
    subject: str
    id: int
    # firstname
    # lastname
    # homework

class ScheduleModel(BaseModel):
    start: int
    end: int

class DayModel(BaseModel):
    available: bool
    name: str
    schedule: List[ScheduleModel]

class WeekModel(BaseModel):
    Pn: List[DayModel]
    Wt: List[DayModel]
    Śr: List[DayModel]
    Cz: List[DayModel]
    Pt: List[DayModel]
    Sb: List[DayModel]
    Nd: List[DayModel]

class CreateNewClass(BaseModel):
    subject: str
    rank: str
    tutor_id: Optional[int] = None
    availability: WeekModel

class Tutor(BaseModel):
    tutor_id: int
    class_id: int
    firstname: str
    lastname: str
    picture: str
    # count_lessons: int
    rank: str

class CreateNewClassStudent(BaseModel):
    month: str
    year: int
    day_name: str
    day: int
    hour: int
    available_class_id: int

class BuyLesson(BaseModel):
    month: str
    year: int
    day_name: str
    day: int
    hour: int
    class_id: int