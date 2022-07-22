from app import oauth2
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
    SELECT day, hour
    FROM 
    (SELECT join_schedules.class_id as j_id, hour, day
    FROM join_schedules, schedules
    WHERE join_schedules.schedules_id = schedules.id) as schedules
    LEFT JOIN classes
    ON schedules.j_id = classes.schedule_id
    WHERE j_id = %s
    """, [class_id])
    schedules = cursor.fetchall()
    return schedules

@router.get("/", response_model=List[schemas.Class])
def get_posts(user_data = Depends(oauth2.get_current_user)):
    if user_data.account_type == 'tutor':
        cursor.execute("""SELECT 
        classes.id as id,
        subject, 
        (SELECT firstname from users where id = classes.student_id), 
        (SELECT lastname from users where id = classes.student_id)
        FROM classes, schedules
        WHERE classes.schedule_id = schedules.id AND tutor_id = %s""",
        (user_data.id,))
        classes = cursor.fetchall()
        return classes

    if user_data.account_type == 'student':
        cursor.execute("""SELECT 
        classes.id,
        subject, 
        (SELECT firstname from users where id = classes.tutor_id), 
        (SELECT lastname from users where id = classes.tutor_id)
        FROM classes, schedules
        WHERE classes.schedule_id = schedules.id AND student_id = %s""",
        (user_data.id,))
        classes = cursor.fetchall()
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
        subject
        FROM classes
        WHERE student_id = %s AND classes.id = %s""",
        (user_data.id, class_id,))
        classes = cursor.fetchall()
        return classes