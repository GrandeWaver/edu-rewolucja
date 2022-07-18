from app import oauth2
from .. import schemas
from fastapi import Depends, HTTPException, status, APIRouter
from ..database import *

router = APIRouter(
    prefix="/posts",
    tags=['Post']
    )

@router.get("/{class_id}")
def get_posts(class_id: int, user_data = Depends(oauth2.get_current_user)):
    cursor.execute("""SELECT * FROM posts WHERE class_id = %s order by created_at desc""", [class_id])
    posts = cursor.fetchall()
    return posts

@router.get("/schedules/{class_id}") # terminy zajęć do konkretnych lekcji
def get_posts(class_id: int, user_data = Depends(oauth2.get_current_user)):
    cursor.execute("""
    SELECT id as class_id, day, hour
    FROM 
    (SELECT join_schedules.class_id as j_id, hour, day
    FROM join_schedules, schedules
    WHERE join_schedules.schedules_id = schedules.id) as schedules
    LEFT JOIN classes
    ON schedules.j_id = classes.schedule_id
    WHERE j_id = %s
    """, [class_id])
    schedules = cursor.fetchall()
    return schedules

@router.get("/classes/")
def get_posts(user_data = Depends(oauth2.get_current_user)):
    if user_data.account_type == 'tutor':
        cursor.execute("""SELECT 
        classes.id,
        subject, 
        (SELECT firstname from users where id = classes.student_id), 
        (SELECT lastname from users where id = classes.student_id)
        FROM classes, schedules
        WHERE classes.schedule_id = schedules.id AND tutor_id = %s""",
        (user_data.id,))
        classes = cursor.fetchall()
        return classes

    if user_data.account_type == 'student':
        cursor.execute("""SELECT 
        classes.id,
        subject, 
        (SELECT firstname from users where id = classes.tutor_id), 
        (SELECT lastname from users where id = classes.tutor_id)
        FROM classes, schedules
        WHERE classes.schedule_id = schedules.id AND student_id = %s""",
        (user_data.id,))
        classes = cursor.fetchall()
        return classes


@router.get("/classes/{class_id}")
def get_posts(class_id: int, user_data = Depends(oauth2.get_current_user)):
    if user_data.account_type == 'tutor':
        cursor.execute("""SELECT 
        classes.id,
        subject, 
        (SELECT firstname from users where id = classes.student_id), 
        (SELECT lastname from users where id = classes.student_id)
        FROM classes, schedules
        WHERE classes.schedule_id = schedules.id AND tutor_id = %s AND classes.id = %s""",
        (user_data.id, class_id,))
        classes = cursor.fetchall()
        return classes

    if user_data.account_type == 'student':
        cursor.execute("""SELECT 
        classes.id,
        subject, 
        (SELECT firstname from users where id = classes.tutor_id), 
        (SELECT lastname from users where id = classes.tutor_id),
        (SELECT day from schedules where id = classes.schedule_id)
        FROM classes, schedules
        WHERE classes.schedule_id = schedules.id AND student_id = %s AND classes.id = %s""",
        (user_data.id, class_id,))
        classes = cursor.fetchall()
        return classes


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_posts(post: schemas.Post, user_data = Depends(oauth2.get_current_user)):
    cursor.execute("""INSERT INTO posts (title, content, published, class_id) VALUES (%s, %s, %s, %s) RETURNING * """, 
    (post.title, post.content, post.published, post.class_id))

    conn.commit()
    new_post = cursor.fetchone()

    return new_post