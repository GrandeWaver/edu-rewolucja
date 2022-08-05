from app import oauth2
from app.utils import format_data
from .. import schemas
from fastapi import Depends, HTTPException, status, APIRouter
from typing import List
from ..database import *

router = APIRouter(
    prefix="/classes",
    tags=['Class']
    )

@router.get("/schedules/{class_id}", response_model=List[schemas.Schedule])
def get_posts(class_id: int, user_data = Depends(oauth2.get_current_user)):
    cursor.execute("""
            SELECT date FROM lessons WHERE class_id = %s AND status = 'planned' ORDER BY date
    """, (class_id,))
    data = cursor.fetchall()

    if len(data) == 0:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"You have no scheduled lessons")

    data = format_data(data)
    return data

@router.get("/", response_model=List[schemas.Class])
def get_posts(user_data = Depends(oauth2.get_current_user)):
    if user_data.account_type == 'tutor':
        cursor.execute("""SELECT 
        classes.id as id,
        subject, 
        (SELECT firstname from users where id = classes.student_id), 
        (SELECT lastname from users where id = classes.student_id),
        (SELECT picture from users where id = classes.student_id)
        FROM classes
        WHERE tutor_id = %s""",
        (user_data.id,))
        classes = cursor.fetchall()
        return classes

    if user_data.account_type == 'student':
        cursor.execute("""SELECT 
        classes.id,
        subject, 
        (SELECT firstname from users where id = classes.tutor_id), 
        (SELECT lastname from users where id = classes.tutor_id),
        (SELECT picture from users where id = classes.tutor_id)
        FROM classes
        WHERE student_id = %s""",
        (user_data.id,))
        classes = cursor.fetchall()

        if len(classes) == 0:
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"You have no classes")

        return classes

@router.get("/details/{class_id}", response_model=List[schemas.ClassDetails])
def get_class_details(class_id: int, user_data = Depends(oauth2.get_current_user)):
    if user_data.account_type == 'tutor':
        cursor.execute("""SELECT 
        id,
        subject
        FROM classes
        WHERE tutor_id = %s AND classes.id = %s""",
        (user_data.id, class_id,))
        classes = cursor.fetchall()
        return classes

    if user_data.account_type == 'student':
        cursor.execute("""SELECT 
        id,
        subject
        FROM classes
        WHERE student_id = %s AND classes.id = %s""",
        (user_data.id, class_id,))
        classes = cursor.fetchall()
        return classes