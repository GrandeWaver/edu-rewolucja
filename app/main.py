from ast import While
from multiprocessing import Pool
import functools
from fastapi import FastAPI, APIRouter, BackgroundTasks
from fastapi_utils.tasks import repeat_every

from app.routers.auth import auth
from app.utils import smap
from .routers import create_class, select_class, frontend, resources, user, post, auth, class_, lesson
from datetime import datetime, date, timedelta
import time
from .database import *
from fastapi.middleware.cors import CORSMiddleware
from .emails.lesson_ten_minutes import mail_student, mail_tutor
from .emails.email_data import get_email_data


app = FastAPI()
app.include_router(frontend.router)
app.include_router(user.router)
app.include_router(post.router)
app.include_router(class_.router)
app.include_router(create_class.router)
app.include_router(select_class.router)
app.include_router(auth.router)
app.include_router(lesson.router)
app.include_router(resources.router)

origins = [
    "http://localhost:8080",
    "https://korki.edu-rewolucja.pl"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/root")
def helloWorld():
    return """Hello World!"""


@app.on_event("startup")
@repeat_every(seconds=59, wait_first=False)
def check_lessons():
    if datetime.now().second != 0:
        # print(f'I am waiting until second == 0; now: {datetime.now().second}')
        time.sleep(60 - datetime.now().second)
        now = datetime.now()
        now = datetime.fromisoformat(str(now)[0:19])

    # print(f'Check lessons - { datetime.now() }')

    cursor.execute("""SELECT * FROM lessons""")
    lessons = cursor.fetchall()

    for lesson in lessons:
        lesson_time = datetime.fromisoformat(str(lesson['date'])[0:19])

        # 10 minuts before lesson
        if now == (lesson_time - timedelta(minutes=10)):
            student, tutor, subject = get_email_data(class_id = lesson['class_id'])

            mail_student_func = functools.partial(mail_student, student['email'], student['firstname'], tutor['firstname'], tutor['lastname'], subject['subject'], lesson_time)
            mail_tutor_func = functools.partial(mail_tutor, tutor['email'], tutor['firstname'], student['firstname'], student['lastname'], subject['subject'], lesson_time)

            with Pool() as pool:
                pool.map(smap, [mail_student_func, mail_tutor_func])
                print('wysłano powiadomienia o lekcjach')
        
        # start lesson
        if now == lesson_time:
            print(f'Rozpoczyna się lekcja {lesson["id"]}')


        # cancel lesson
        if lesson_time < now and lesson['status'] != 'after' and lesson['status'] != 'canceled':
            cursor.execute("""
                UPDATE lessons SET status = 'canceled' WHERE id = %s
            """, (lesson['id'],))
            print(f'Anulowano lekcje o id: {lesson["id"]}')

    conn.commit()

# cursor.execute("""
#     UPDATE lessons SET status = 'now' WHERE id = %s
# """, (lesson['id'],))