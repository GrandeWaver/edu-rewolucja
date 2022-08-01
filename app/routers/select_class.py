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

    if len(tutors) == 0:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"No tutors available")

    return tutors

@router.get("/schedules/{available_class_id}") #, response_model=List[schemas.Tutor]
def get_schedules(available_class_id: int, user_data = Depends(oauth2.get_current_user)):
    days = ["Pn","Wt","Śr","Cz","Pt","Sb","Nd"]
    months = ["styczeń", "luty", "marzec", "kwiecień", "maj", "czerwiec", "lipiec", "sierpień", "wrzesień", "październik", "listopad", "grudzień", ]

    cursor.execute("""
        SELECT available_tutor_schedule_id, tutor_id FROM available_classes WHERE id = %s
    """, (available_class_id,))
    available_tutor_schedule_id = cursor.fetchone()

    cursor.execute("""
        SELECT day, schedule_id
        FROM available_tutor_schedules, join_tutor_week
        WHERE join_tutor_week.available_day_id = available_tutor_schedules.id
        AND join_tutor_week.week_id = %s;
    """, (available_tutor_schedule_id['available_tutor_schedule_id'],))
    row_data = cursor.fetchall()

    # dni tygodnia ORAZ godziny pracy
    working_days = []
    working_hours = []
    day_index = - 1
    for item in row_data:
        day_index = day_index + 1
        working_days.append(item['day'])
        hours_row = {'day': item['day'], 'working_hours': []}
        working_hours.append(hours_row)
        cursor.execute("""
            SELECT start_at, end_at
            FROM schedule_array, available_tutor_schedules
            WHERE schedule_array.schedule_id = available_tutor_schedules.schedule_id
            AND available_tutor_schedules.schedule_id = %s;
        """, (item['schedule_id'],))
        sql = cursor.fetchall()
        for start_end in sql:
            # append to working_hours
            hours = make_scope(start_end['start_at'], start_end['end_at'])
            working_hours[day_index]['working_hours'] = working_hours[day_index]['working_hours'] + hours

        working_hours[day_index]['working_hours'].pop()

        
    # dni tygodnia ORAZ daty 90 dni
    ninety_days = []
    today = datetime.now()
    count = 0
    for n in range(90):
        day = (today+timedelta(days=1)) + timedelta(days=count)
        week_day = days[day.weekday()]
        date = day.isoformat()
        row = {'day': week_day, 'date': date}
        ninety_days.append(row)
        count = count + 1

    # tylko te dni tygodnia ORAZ daty w które pracuje tutor
    working_90_days= []
    working_months = []

    for item in ninety_days:
        for element in working_days:
            if element == item['day']:
                month_number = item['date'][5:7]
                month = months[int(month_number)-1]
                day_number = item['date'][8:10]
                row_days = {'month': month, 'day': item['day'], 'date': day_number}
                working_90_days.append(row_days)
                row_months = {'month': month, 'year': item['date'][2:4]}
                working_months.append(row_months)
  
    working_months = remove_repetitions(working_months)

    cursor.execute("""
        SELECT date 
        FROM lessons, classes 
        WHERE lessons.class_id = classes.id
        AND classes.tutor_id = %s
    """, (available_tutor_schedule_id['tutor_id'],))
    busy_days = cursor.fetchall()

    busy = []
    for day in busy_days:
        day_number = str(day['date'])[8:10]
        month = months[int(str(day['date'])[5:7])-1]
        hour = int(str(day['date'])[11:13])
        row = {'month': month, 'date': day_number, 'hour': hour}
        busy.append(row)

    dict = []
    month_index = -1
    for month in working_months:
        month_index = month_index + 1
        month_row = {'month': month['month'], 'month_index': month_index, 'year': month['year'], 'days': []}
        dict.append(month_row)
        day_index = -1
        for day in working_90_days:
            if month['month'] == day['month']:
                for schedule in working_hours:
                    if schedule['day'] == day['day']:
                        day_index = day_index + 1
                        # skasuj wszystkie godziny w które tutor ma już zaplanowane lekcje
                        # print(f"{day['month']} {day['date']} {day['day']}: {schedule['working_hours']}")
                        for element in busy:
                            if day['month'] == element['month']:
                                if day['date'] == element['date']:
                                    for item in schedule['working_hours']:
                                        if item == element['hour']:
                                            schedule['working_hours'].remove(item)
                        day_row = {'day': day['date'], 'day_index': day_index, 'name': day['day'], 'working_hours': schedule['working_hours']}
                        dict[month_index]['days'].append(day_row)
    # print(busy)
    return dict