from sqlalchemy import true
from .. import utils, schemas
from pathlib import Path
from ..database import *
from fastapi import HTTPException, status, APIRouter
from pydantic import EmailStr
from fastapi.responses import FileResponse, RedirectResponse

BASE_DIR = Path(__file__).resolve().parent

router = APIRouter(
    prefix="/users",
    tags=['User']
    )

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate):
    # whether the user is already in the database
    cursor.execute("""SELECT * FROM users WHERE email = %s""", (user.email,))
    user_check = cursor.fetchone()

    if len(user.firstname) == 0:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Empty field: firstname")

    if len(user.lastname) == 0:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Empty field: lastname")

    elif user_check:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User already exists")
    
    elif len(user.password) < 6:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Password is too short")
    



    user.password = utils.hash(user.password)

    cursor.execute("""INSERT INTO users (email, firstname, lastname, password) VALUES (%s, %s, %s, %s) RETURNING * """, 
    (user.email, user.firstname, user.lastname, user.password))

    conn.commit()
    new_user = cursor.fetchone()

    return new_user


@router.post('/check')
def check_email(email: schemas.Email):
    cursor.execute("""SELECT * FROM users WHERE email = %s""", (email.email,))
    user = cursor.fetchone()
    if user:
        if user['sub'] != None:
            return {'response': 'google_user'}
        else:
            return {'response': 'true'}
    else:
        return {'response': 'false'}


@router.get('/details/{id}', response_model=schemas.UserOut)
def get_user(id: int):
    cursor.execute("""SELECT * FROM users WHERE id = %s""", (id,))
    user = cursor.fetchone()
    return user


@router.get('/picture/{id}')
def get_photo(id: int):
    cursor.execute("""SELECT picture FROM users WHERE id = %s""", (id,))
    photo_link = cursor.fetchone()
    return RedirectResponse(photo_link["picture"])

@router.get('/picture-from-email/{email}')
def get_photo(email: EmailStr):
    cursor.execute("""SELECT picture FROM users WHERE email = %s""", (email,))
    photo_link = cursor.fetchone()
    return {"picture": photo_link["picture"]}


@router.get("/defaultpicture")
def image_endpoint():
    path =str(Path(BASE_DIR, 'images'))
    file_path = os.path.join(path, 'avatar.jpg')
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"File not found")
