from os import access
from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from app.create_meeting import generateToken
from ..database import *
from .. import schemas, utils, oauth2

router = APIRouter(
    prefix="/auth",
    tags=['Authentication']
)

@router.post('/')
def auth(user_credentials: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm)):

    cursor.execute("""SELECT * FROM users WHERE email = %s""", (user_credentials.username,))
    user = cursor.fetchone()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user['password']):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    access_token = oauth2.create_access_token(data={"user_id": user['id'], "account_type": user['account_type'], "picture": user['picture']})
    return {'access_token': access_token, "token_type": "bearer"}

@router.get('/')
def check_auth(user_data = Depends(oauth2.get_current_user)):
    return user_data


@router.post('/googleuser', response_model=schemas.Token)
def google_user(token: schemas.GoogleToken):
    
    # verify token
    token_data = oauth2.validate_security_token(token.token, oauth2.client_ids)
    
    cursor.execute("""SELECT * FROM users WHERE sub = %s""", (token_data["sub"],))
    user_db = cursor.fetchone()
    if user_db:
        cursor.execute("""UPDATE users SET email = %s, firstname = %s, lastname = %s, picture = %s, email_verified = %s where sub = %s RETURNING * """, 
            (token_data["email"], token_data["given_name"], token_data["family_name"], token_data["picture"], token_data["email_verified"], token_data["sub"],))

        conn.commit()
        logged_user = cursor.fetchone()
        if logged_user:
            # succes
            access_token = oauth2.create_access_token(data={"user_id": logged_user['id'], "account_type": logged_user['account_type'], "picture": logged_user['picture']})
            return {'access_token': access_token, "token_type": "bearer"}
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"database error")
    else:
        cursor.execute("""SELECT * FROM users WHERE email = %s""", (token_data["email"],))
        email_repeated = cursor.fetchone()
        if email_repeated:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"user has already signed up with email (cannot signup with google)")
        else:
            cursor.execute("""INSERT INTO users (email, firstname, lastname, picture, sub, email_verified) VALUES (%s, %s, %s, %s, %s, %s) RETURNING * """, 
            (token_data["email"], token_data["given_name"], token_data["family_name"], token_data["picture"], token_data["sub"], token_data["email_verified"],))

            conn.commit()
            new_user = cursor.fetchone()
            if new_user:
                # succes
                access_token = oauth2.create_access_token(data={"user_id": new_user['id'], "account_type": new_user['account_type'], "picture": new_user['picture']})
                return {'access_token': access_token, "token_type": "bearer"}
            else:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"database error")


import requests
import json
import base64
from app.create_meeting import *

@router.get('/zoomuser')
def zoom_user(code: str):
    encoded_authorization_key = base64.b64encode(f'{API_KEY}:{API_SEC}'.encode('ascii'))
    print(encoded_authorization_key)

    headers = { "Authorization": "Basic WXVETUJ1Zm1SbW1TaV9IOGlHeW9OQTpxSEUyNHpVaERmWGxRWWVOcGNvS2lHazBLa0w4YjR5Mg=="}
    r = requests.post(
        f'https://zoom.us/oauth/token?grant_type=authorization_code&code={code}&redirect_uri=https://app.edu-rewolucja.pl/auth/zoomuser', headers=headers)

    print("\n creating zoom meeting ... \n")
    data = json.loads(r.text)

    return {"code": code, "data": data}