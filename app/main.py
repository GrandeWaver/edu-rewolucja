from ast import While
from fastapi import FastAPI, APIRouter
from fastapi_utils.tasks import repeat_every

from app.routers.auth import auth
from .routers import create_class, select_class, frontend, resources, user, post, auth, class_, lesson
from datetime import datetime, date
import time
from .database import *
from fastapi.middleware.cors import CORSMiddleware


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
@repeat_every(seconds=60, wait_first=False)
def check_lessons():
    
    # zero = datetime.now().minute
    # while zero != 0:
    #     print('Debug: konfigurowanie równej godziny')
    #     time.sleep(1)
    #     zero = datetime.now().minute

    print(f'check lessons: {datetime.now()}')

    cursor.execute("""
        SELECT * FROM lessons
    """)
    lessons = cursor.fetchall()

    now = datetime.now()
    now = datetime.fromisoformat(str(now)[0:19])

    for i in lessons:
        lesson_time = datetime.fromisoformat(str(i['date'])[0:19])
        print(now)
        print(lesson_time)
        if lesson_time == now:
            cursor.execute("""
                UPDATE lessons SET status = 'now' WHERE id = %s
            """, (i['id'],))
        if lesson_time < now:
            cursor.execute("""
                UPDATE lessons SET status = 'canceled' WHERE id = %s
            """, (i['id'],))
    conn.commit()

