from re import X
from app import oauth2
from app.utils import *
from .. import schemas
from fastapi import Depends, HTTPException, status, APIRouter
from typing import List
from ..database import *
from datetime import datetime, timedelta
import json
from ..emails.lesson_created import mail_lesson_created

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
def get_available_class_id(data: schemas.BuyLesson, user_data = Depends(oauth2.get_current_user)):
    print(f'-----------------------------{data}------------------------------')
    
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

    cursor.execute("""SELECT email, firstname FROM users WHERE id = %s """, (user_data.id,))
    receiver_email = cursor.fetchone()

    mail_lesson_created(receiver_email['email'], receiver_email['firstname'], data)

    return data