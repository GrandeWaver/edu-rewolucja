from re import X
from app import oauth2
from app.utils import *
from .. import schemas
from fastapi import Depends, HTTPException, status, APIRouter, BackgroundTasks
from typing import List
from ..database import *
from datetime import datetime, timedelta
import json
from ..emails.lesson_created import mail_student, mail_tutor

router = APIRouter(
    prefix="/lesson",
    tags=['Lesson']
    )

@router.get("/get-available-class-id/{class_id}")
def get_available_class_id(class_id: int, user_data = Depends(oauth2.get_current_user)):
    cursor.execute("""
        SELECT source_available_class_id, subject FROM classes WHERE id = %s
    """, (class_id,))

    source_available_class_id = cursor.fetchone()

    return source_available_class_id


@router.post("/", status_code=status.HTTP_201_CREATED)
async def get_available_class_id(background_tasks: BackgroundTasks, data: schemas.BuyLesson, user_data = Depends(oauth2.get_current_user)):

    # konwertowanie tego na date
    months = ["styczeń", "luty", "marzec", "kwiecień", "maj", "czerwiec", "lipiec", "sierpień", "wrzesień", "październik", "listopad", "grudzień", ]
    month = months.index(data.month)
    month = month + 1

    date_str = str(data.day)+'/'+str(month)+'/'+str(data.year)+' '+str(data.hour)+':00:00'
    date = datetime.strptime(date_str, "%d/%m/%y %H:%M:%S")

    cursor.execute("""SELECT now() AT TIME ZONE 'Europe/Warsaw'""")
    create_at_date = cursor.fetchone()

    # INSERT INTO LESSONS
    cursor.execute("""
        INSERT INTO lessons (date, created_at, status, class_id) VALUES(%s, %s, %s, %s) RETURNING *
    """, (date, create_at_date['timezone'], 'planned', data.class_id))

    conn.commit()

    # emails
    cursor.execute("""SELECT email, firstname, lastname FROM users WHERE id = %s """, (user_data.id,))
    student = cursor.fetchone()

    cursor.execute("""SELECT subject FROM classes WHERE id = %s""", (data.class_id,))
    subject = cursor.fetchone()

    cursor.execute("""
    SELECT  email, firstname, lastname
    FROM users, classes
    WHERE classes.tutor_id = users.id
    AND classes.id = %s
    """, (data.class_id,))

    tutor = cursor.fetchone()



    background_tasks.add_task(mail_student, student['email'], student['firstname'], tutor['firstname'], tutor['lastname'], data, subject['subject'])
    background_tasks.add_task(mail_tutor, tutor['email'], tutor['firstname'], student['firstname'], student['lastname'], data, subject['subject'])

    return data