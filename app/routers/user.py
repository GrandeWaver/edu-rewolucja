from .. import utils, schemas
from ..database import *
from fastapi import status, APIRouter


router = APIRouter(
    prefix="/users",
    tags=['User']
    )

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate):

    user.password = utils.hash(user.password)

    cursor.execute("""INSERT INTO users (email, firstname, lastname, password) VALUES (%s, %s, %s, %s) RETURNING * """, 
    (user.email, user.firstname, user.lastname, user.password))

    conn.commit()
    new_user = cursor.fetchone()

    return new_user


@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int):
    cursor.execute("""SELECT * FROM users WHERE id = %s""", (id,))
    user = cursor.fetchone()
    return user