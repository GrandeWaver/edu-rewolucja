from app import oauth2
from .. import schemas
from fastapi import Depends, status, APIRouter
from ..database import *

router = APIRouter(
    prefix="/posts",
    tags=['Post']
    )

@router.get("/")
def get_posts(user_data = Depends(oauth2.get_current_user)):
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_posts(post: schemas.Post, user_data = Depends(oauth2.get_current_user)):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
    (post.title, post.content, post.published))

    conn.commit()
    new_post = cursor.fetchone()

    return new_post