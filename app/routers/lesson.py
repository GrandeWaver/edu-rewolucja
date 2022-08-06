from re import X
from app import oauth2
from app.utils import *
from .. import schemas
from fastapi import Depends, HTTPException, status, APIRouter
from typing import List
from ..database import *
from datetime import datetime, timedelta
import json

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

    print(f'**************************{date}***************************')

    # INSERT INTO LESSONS
    cursor.execute("""
        INSERT INTO lessons (date, status, class_id) VALUES(%s, %s, %s) RETURNING *
    """, (date, 'planned', data.class_id))

    conn.commit()

    return data