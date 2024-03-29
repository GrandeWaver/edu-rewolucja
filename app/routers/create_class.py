from hashlib import new
from app import oauth2
from .. import schemas
from fastapi import Depends, HTTPException, status, APIRouter, BackgroundTasks
from ..database import *
from datetime import datetime
from ..emails.class_created import mail_student, mail_tutor

router = APIRouter(
    prefix="/create_class",
    tags=['Create Class']
    )

@router.post("/tutor", status_code=status.HTTP_201_CREATED)
def create_posts(data: schemas.CreateNewClass, user_data = Depends(oauth2.get_current_user)):

    tutor_id = user_data.id
    subject = data.subject
    rank = data.rank
    price_tutor = data.price
    price_netto = price_tutor # + 10

    availability = data.availability #potrzebne w eval()
    days = ["Pn","Wt","Śr","Cz","Pt","Sb","Nd"]

    cursor.execute("""SELECT id FROM available_classes WHERE tutor_id = %s AND subject = %s""", (tutor_id, subject))
    is_already = cursor.fetchone()
    if is_already != None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"You have already created this class")

    available_check = []
    for day in days:
        available = eval(f'availability.{day}[0].available')
        if available == False:
            available_check.append('.')
    if len(available_check) == 7:
        raise HTTPException(status_code=status.HTTP_418_IM_A_TEAPOT, detail=f"You are very lazy :p")

    cursor.execute("""SELECT week_id as max_week_id FROM join_tutor_week ORDER BY max_week_id desc LIMIT 1""", []) # INIT: musi być pierwszy wiersz
    max_week_id = cursor.fetchone()
    max_week_id = int(max_week_id['max_week_id']) + 1

    for day in days:
        WeekItems = eval(f'availability.{day}[0].schedule')
        available = eval(f'availability.{day}[0].available')

        if available == False:
            print('available == false, skipping day')
        else:
            cursor.execute("""SELECT MAX(schedule_id) as max_schedule_id FROM schedule_array""") # INIT: musi być pierwszy wiersz
            schedule_id_for_day = cursor.fetchone()
            schedule_id_for_day = int(schedule_id_for_day['max_schedule_id']) + 1

            for i in WeekItems:
                cursor.execute("""INSERT INTO schedule_array (schedule_id, start_at, end_at) VALUES (%s, %s, %s) RETURNING * """,
                (schedule_id_for_day, i.start, i.end))
                start_end_id = cursor.fetchone()
                print(f'start_end: {start_end_id}')
        
            cursor.execute("""INSERT INTO available_tutor_schedules (day, schedule_id) VALUES (%s, %s) RETURNING * """,
            (day, start_end_id['schedule_id']))
            array_id = cursor.fetchone()

            available_day_id = array_id['id']
            cursor.execute("""INSERT INTO join_tutor_week (week_id, available_day_id) VALUES (%s, %s) RETURNING * """,
            (max_week_id, available_day_id))

            available_tutor_schedule_id = cursor.fetchone() # POTEM WYKORZYSTAMY GO W INNYCH DNIACH TYGODNIA

    cursor.execute("""INSERT INTO available_classes (subject, rank, tutor_id, available_tutor_schedule_id, price_tutor, price_netto) VALUES (%s, %s, %s, %s, %s, %s) RETURNING * """,
    (subject, rank, tutor_id, available_tutor_schedule_id['week_id'], price_tutor, price_netto))

    conn.commit()
    new_available_class = cursor.fetchone()


    return new_available_class

@router.post("/student", status_code=status.HTTP_201_CREATED)
def create_posts(background_tasks: BackgroundTasks, data: schemas.CreateNewClassStudent, user_data = Depends(oauth2.get_current_user)):

    # konwertowanie tego na date
    months = ["styczeń", "luty", "marzec", "kwiecień", "maj", "czerwiec", "lipiec", "sierpień", "wrzesień", "październik", "listopad", "grudzień", ]
    month = months.index(data.month)
    month = month + 1

    first_lesson_date_str = str(data.day)+'/'+str(month)+'/'+str(data.year)+' '+str(data.hour)+':00:00'
    first_lesson_date = datetime.strptime(first_lesson_date_str, "%d/%m/%y %H:%M:%S")

    cursor.execute("""
        SELECT * FROM available_classes WHERE id = %s
    """,(data.available_class_id,))
    available_class = cursor.fetchone()

    # szybki check czy ten tutor nie ma już zajęć z tym uczniem i z tym przedmiotem
    cursor.execute("""
        SELECT * FROM classes WHERE subject = %s AND tutor_id = %s AND student_id = %s
    """, (available_class['subject'], available_class['tutor_id'], user_data.id,))
    is_already = cursor.fetchone()

    if is_already != None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"You already have this class")
    
    # INSERT INTO classes
    cursor.execute("""
        INSERT INTO classes (subject, tutor_id, student_id, rank, source_available_class_id) VALUES(%s, %s, %s, %s, %s) RETURNING *
    """, (available_class['subject'], available_class['tutor_id'], user_data.id, available_class['rank'], available_class['id']))

    new_class = cursor.fetchone()

    cursor.execute("""SELECT now() AT TIME ZONE 'Europe/Warsaw'""")
    create_at_date = cursor.fetchone()
    
    # INSERT INTO LESSONS
    cursor.execute("""
        INSERT INTO lessons (date, created_at, status, class_id) VALUES(%s, %s, %s, %s) RETURNING *
    """, (first_lesson_date, create_at_date['timezone'], 'planned', new_class['id']))

    conn.commit()

    #emails
    cursor.execute("""SELECT email, firstname, lastname FROM users WHERE id = %s """, (user_data.id,))
    student = cursor.fetchone()

    cursor.execute("""SELECT subject FROM classes WHERE id = %s""", (new_class['id'],))
    subject = cursor.fetchone()

    cursor.execute("""
    SELECT  email, firstname, lastname
    FROM users, classes
    WHERE classes.tutor_id = users.id
    AND classes.id = %s
    """, (new_class['id'],))

    tutor = cursor.fetchone()


    background_tasks.add_task(mail_student, student['email'], student['firstname'], tutor['firstname'], tutor['lastname'], data, subject['subject'])
    background_tasks.add_task(mail_tutor, tutor['email'], tutor['firstname'], student['firstname'], student['lastname'], data, subject['subject'])


    return data