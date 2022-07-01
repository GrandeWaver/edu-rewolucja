from fastapi import Depends, status, HTTPException
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security.oauth2 import OAuth2PasswordBearer

import sys, os
from app import schemas
sys.path.append(os.path.abspath('../../'))
import secret

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth')

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=secret.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, secret.SECRET_KEY, algorithm=secret.ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentials_exeption):
    try:
        payload = jwt.decode(token, secret.SECRET_KEY, algorithms=[secret.ALGORITHM])
        id: str = payload.get("user_id")
        account_type: str = payload.get("account_type")

        if id is None:
            raise credentials_exeption
        token_data = schemas.TokenData(id=id, account_type=account_type)
    except JWTError:
        raise credentials_exeption
    
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exeption = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    return verify_access_token(token, credentials_exeption)