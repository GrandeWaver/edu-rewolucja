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