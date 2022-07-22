from app import oauth2
from .. import schemas
from fastapi import Depends, HTTPException, status, APIRouter
from ..database import *

router = APIRouter(
    prefix="/create_class",
    tags=['Create Class']
    )

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_posts(data: schemas.CreateNewClass, user_data = Depends(oauth2.get_current_user)):

    tutor_id = data.tutor_id
    subject = data.subject
    rank = data.rank
    availability = data.availability #potrzebne w eval()
    days = ["Pn","Wt","Śr","Cz","Pt","Sb","Nd"]

    available_check = []
    for day in days:
        available = eval(f' availability.{day}[0].available')
        if available == False:
            available_check.append('.')
    if len(available_check) == 7:
        raise HTTPException(status_code=status.HTTP_418_IM_A_TEAPOT, detail=f"You are very lazy :p")


    print(f"tutor_id: {tutor_id}")
    print(f"subject: {subject}")
    print(f"rank: {rank}")


    cursor.execute("""SELECT week_id as max_week_id FROM join_tutor_week ORDER BY max_week_id desc LIMIT 1""", []) # INIT: musi być pierwszy wiersz
    max_week_id = cursor.fetchone()
    max_week_id = int(max_week_id['max_week_id']) + 1

    for day in days:
        WeekItems = eval(f' availability.{day}[0].schedule')
        available = eval(f' availability.{day}[0].available')

        if available == False:
            print('available == false, skip day')
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
            print(f'available_tutor_schedules: {array_id}')

            available_day_id = array_id['id']
            cursor.execute("""INSERT INTO join_tutor_week (week_id, available_day_id) VALUES (%s, %s) RETURNING * """,
            (max_week_id, available_day_id))

            available_tutor_schedule_id = cursor.fetchone() # POTEM WYKORZYSTAMY GO W INNYCH DNIACH TYGODNIA!
            print(f'available_tutor_schedule_id: {available_tutor_schedule_id}')

    cursor.execute("""INSERT INTO available_classes (subject, rank, tutor_id, available_tutor_schedule_id) VALUES (%s, %s, %s, %s) RETURNING * """,
    (subject, rank, tutor_id, available_tutor_schedule_id['week_id']))

    conn.commit()
    new_available_class = cursor.fetchone()


    return new_available_class