from os import access
from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..database import *
from .. import schemas, utils, oauth2

router = APIRouter(
    prefix="/auth",
    tags=['Authentication']
)

@router.post('/')
def auth(user_credentials: OAuth2PasswordRequestForm = Depends()):

    cursor.execute("""SELECT * FROM users WHERE email = %s""", (user_credentials.username,))
    user = cursor.fetchone()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user['password']):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    access_token = oauth2.create_access_token(data={"user_id": user['id'], "account_type": user['account_type']})
    return {'access_token': access_token, "token_type": "bearer"}

@router.get('/')
def check_auth(user_data = Depends(oauth2.get_current_user)):
    return user_data


@router.post('/googleuser', response_model=schemas.Token)
def google_user(user: schemas.GoogleUser):
    # verify token
    if user.iss == 'https://accounts.google.com':
        cursor.execute("""SELECT * FROM users WHERE sub = %s""", (user.sub,))
        user_db = cursor.fetchone()
        if user_db:
            cursor.execute("""UPDATE users SET email = %s, firstname = %s, lastname = %s, picture = %s, email_verified = %s where sub = %s RETURNING * """, 
                (user.email, user.firstname, user.lastname, user.picture, user.email_verified, user.sub,))

            conn.commit()
            logged_user = cursor.fetchone()
            if logged_user:
                # succes
                access_token = oauth2.create_access_token(data={"user_id": logged_user['id'], "account_type": logged_user['account_type']})
                return {'access_token': access_token, "token_type": "bearer"}
            else:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"database error")
        else:
            cursor.execute("""SELECT * FROM users WHERE email = %s""", (user.email,))
            email_repeated = cursor.fetchone()
            if email_repeated:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"user has already signed up with email (cannot signup with google)")
            else:
                cursor.execute("""INSERT INTO users (email, firstname, lastname, picture, sub, email_verified) VALUES (%s, %s, %s, %s, %s, %s) RETURNING * """, 
                (user.email, user.firstname, user.lastname, user.picture, user.sub, user.email_verified,))

                conn.commit()
                new_user = cursor.fetchone()
                if new_user:
                    # succes
                    access_token = oauth2.create_access_token(data={"user_id": new_user['id'], "account_type": new_user['account_type']})
                    return {'access_token': access_token, "token_type": "bearer"}
                else:
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"database error")
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"iss is not from google.com")
