from app import oauth2
from .. import schemas
from fastapi import Depends, HTTPException, status, APIRouter
from typing import List
from ..database import *

router = APIRouter(
    prefix="/posts",
    tags=['Post']
    )

@router.get("/{class_id}", response_model=List[schemas.Post])
def get_posts_for_class(class_id: int, user_data = Depends(oauth2.get_current_user)):
    cursor.execute("""SELECT id, title, content, created_at FROM posts WHERE class_id = %s AND published = true order by created_at desc""", [class_id])
    posts = cursor.fetchall()
    return posts

@router.get("/details/{post_id}", response_model=List[schemas.PostDetails])
def get_post_details(post_id: int, user_data = Depends(oauth2.get_current_user)):
    cursor.execute("""SELECT id, class_id, title, content, created_at FROM posts WHERE id = %s AND published = true order by created_at desc""", [post_id])
    post = cursor.fetchall()
    return post

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_posts(post: schemas.NewPost, user_data = Depends(oauth2.get_current_user)):
    cursor.execute("""INSERT INTO posts (title, content, class_id) VALUES (%s, %s, %s) RETURNING * """, 
    (post.title, post.content, post.class_id))

    conn.commit()
    new_post = cursor.fetchone()

    return new_post