from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every

from app.routers.auth import auth
from .routers import create_class, select_class, frontend, resources, user, post, auth, class_, lesson, notifications
from datetime import datetime, timedelta
import time
from .database import *
from fastapi.middleware.cors import CORSMiddleware

from .emails.email_data import get_email_data
from app.registry import registry


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
app.include_router(notifications.router)

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
        time.sleep(60 - datetime.now().second)
        now = datetime.now()
        now = datetime.fromisoformat(str(now)[0:19])

    cursor.execute("""SELECT * FROM lessons""")
    lessons = cursor.fetchall()

    for lesson in lessons:
        lesson_time = datetime.fromisoformat(str(lesson['date'])[0:19])

        # 10 minuts before lesson
        if now == (lesson_time - timedelta(minutes=10)):
            print(f'Lekcja o id: {lesson["id"]} zacznie się za 10 minut')

            student, tutor, subject = get_email_data(lesson['class_id'])

            registry.add_ten_to_lesson(
                tutor['id'], 
                tutor['email'],
                tutor['firstname'], 
                tutor['lastname'], 
                student['id'], 
                student['email'],
                student['firstname'], 
                student['lastname'],
                lesson_time, 
                subject['subject'],
                lesson['id']
            )
        
        # start lesson
        if (lesson_time + timedelta(minutes=55)) > now and lesson_time <= now:
            active_lessons = registry.return_active_lessons()

            if not any(l['lesson_id'] == lesson['id'] for l in active_lessons):
                print(f'Rozpoczyna się lekcja {lesson["id"]}')

                cursor.execute("""
                    UPDATE lessons SET status = 'now' WHERE id = %s
                """, (lesson['id'],))

                # usun sie z registry ten_to_lesson zeby nie dostawać niepotrzebnego powiadomienia w przyszłości
                ten_to_lesson = registry.return_ten_to_lesson()
                for i in ten_to_lesson:
                    if i['lesson_id'] == lesson["id"]:
                        ten_to_lesson.remove(i)

                # dodaj lekcje do aktywnych lekcji
                student, tutor, subject = get_email_data(lesson['class_id'])
                registry.add_active_lessons(
                    lesson['id'], 
                    tutor['id'], 
                    tutor['firstname'], 
                    tutor['lastname'], 
                    tutor['picture'], 
                    student['id'], 
                    student['firstname'], 
                    student['lastname'], 
                    student['picture']
                )


        # end lesson
        if (lesson_time + timedelta(minutes=55)) < now and lesson['status'] == 'now':
            cursor.execute("""
                UPDATE lessons SET status = 'after' WHERE id = %s
            """, (lesson['id'],))
            print(f'Zakończono lekcje o id: {lesson["id"]}')

            active_lessons = registry.return_active_lessons()
            for i in active_lessons:
                if i['lesson_id'] == lesson["id"]:
                    ten_to_lesson.remove(i)
        
        # cancel lesson
        if (lesson_time + timedelta(minutes=55)) < now and lesson['status'] == 'planned':
            cursor.execute("""
                UPDATE lessons SET status = 'canceled' WHERE id = %s
            """, (lesson['id'],))
            print(f'Anulowano lekcje o id: {lesson["id"]}')

    conn.commit()

# cursor.execute("""
#     UPDATE lessons SET status = 'now' WHERE id = %s
# """, (lesson['id'],))