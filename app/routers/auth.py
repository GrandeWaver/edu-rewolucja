from os import access
from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from ..database import *
from .. import schemas, utils, oauth2
import requests
import json
import base64
from app.create_meeting import *
import sys, os
sys.path.append(os.path.abspath('../../'))
import secret

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

meetingdetails = {"topic": "The title of your zoom meeting",
                  "type": 2,
                  "start_time": "2019-06-14T10: 21: 57",
                  "duration": "45",
                  "timezone": "Europe/Madrid",
                  "agenda": "test",

                  "recurrence": {"type": 1,
                                 "repeat_interval": 1
                                 },
                  "settings": {"host_video": "true",
                               "participant_video": "true",
                               "join_before_host": "False",
                               "mute_upon_entry": "False",
                               "watermark": "true",
                               "audio": "voip",
                               "auto_recording": "cloud"
                               }
                  }

@router.get('/zoomuser')
def zoom_user(code: str):
    encoded_authorization_key = base64.b64encode(f'{secret.ZOOM_API_KEY}:{secret.ZOOM_API_SECRET}'.encode('ascii'))
    encoded_authorization_key = encoded_authorization_key.decode()

    headers = { "Authorization": f"Basic {encoded_authorization_key}"}
    r = requests.post(
        f'https://zoom.us/oauth/token?grant_type=authorization_code&code={code}&redirect_uri=https://app.edu-rewolucja.pl/auth/zoomuser', headers=headers)

    oauth = json.loads(r.text)

    try:
        headers = {'authorization': 'Bearer %s' % oauth['access_token'],
                'content-type': 'application/json'}
        r = requests.get('https://api.zoom.us/v2/users/', headers=headers)

        users = json.loads(r.text)
    except:
        users = {"error": "read logs"}

    try:
        print(users["users"][0]["id"])
        headers = {'authorization': 'Bearer %s' % oauth['access_token'],
                'content-type': 'application/json'}
        r = requests.post(
            f'https://api.zoom.us/v2/users/{users["users"][0]["id"]}/meetings', headers=headers, data=json.dumps(meetingdetails))

        print("\n creating zoom meeting ... \n")
        data = json.loads(r.text)
        if data["code"] == '429':
            return{"data": data}
        else:
            print(data["start_url"])
            print('\n'+data["join_url"])
            print('\n'+data['password'])
    except:
        print("Error: auth.py -> line: 118-130")


    return {"code": code, "data": oauth, "users": users}