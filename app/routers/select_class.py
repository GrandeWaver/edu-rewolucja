from re import X
from app import oauth2
from .. import schemas
from fastapi import Depends, HTTPException, status, APIRouter
from typing import List
from ..database import *
from datetime import datetime, timedelta

router = APIRouter(
    prefix="/select_class",
    tags=['Select Class']
    )

@router.get("/{subject}", response_model=List[schemas.Tutor])
def get_tutors(subject: str, user_data = Depends(oauth2.get_current_user)):
    cursor.execute("""
    SELECT 
    tutor_id,
    ac.id as class_id,
    firstname,
    lastname,
    picture,
    ac.rank
    FROM 
    available_classes as ac, 
    users as u 
    WHERE 
    ac.tutor_id = u.id
    AND
    u.account_type = 'tutor'
    AND
    ac.subject = %s""", [subject])
    # order by count_lessons
    tutors = cursor.fetchall()

    return tutors

@router.get("/schedules/{available_class_id}") #, response_model=List[schemas.Tutor]
def get_schedules(available_class_id: int, user_data = Depends(oauth2.get_current_user)):
    days = ["Pn","Wt","Śr","Cz","Pt","Sb","Nd"]

    cursor.execute("""SELECT * FROM schedule_array""")
    schedules = cursor.fetchone()

    today = datetime.now()
    print('Datetime is:', today)
    weekday_int = today.weekday()
    print('Day of a week is:', days[weekday_int])

    N_DAYS_FORWARD = 90
    n_days_forward = today + timedelta(days=N_DAYS_FORWARD)

    print('Za 90 dni będzie:', days[n_days_forward.weekday()])


    dict = [{
            'month': 'lipiec',
            'month_index': 0,
            'days': 
                [
                    {
                    'day': 26,
                    'day_index': 0,
                    'name': 'Wt',
                    'working_hours': 
                        [11, 12, 13, 14]
                    },
                    {
                    'day': 27,
                    'day_index': 1,
                    'name': 'Śr',
                    'working_hours': 
                        [11, 12, 13, 14, 15, 16]
                    },
                    {
                    'day': 28,
                    'day_index': 2,
                    'name': 'Cz',
                    'working_hours': 
                        [14, 15, 16]
                    }
                ],
        },
        {
            'month': 'sierpień',
            'month_index': 1,
            'days': 
                [
                    {
                    'day': 1,
                    'day_index': 0,
                    'name': 'Wt',
                    'working_hours': 
                        [9, 10, 11]
                    },
                    {
                    'day': 2,
                    'day_index': 1,
                    'name': 'Śr',
                    'working_hours': 
                        [9, 10, 11, 12]
                    },
                ],
        }]

    return dict