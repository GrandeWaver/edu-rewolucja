from fastapi import Depends, status, HTTPException
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security.oauth2 import OAuth2PasswordBearer

import sys, os
from app import schemas
sys.path.append(os.path.abspath('../../'))
import secret

# verify google oauth token
import json
import jwt       # pip install pyjwt
import requests  # pip install requests

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth')
client_ids = ['365589210157-88s142dtgt2e1hd4muaiqbj6bb96dm5b.apps.googleusercontent.com'] # Get your apps' client IDs from the API console:

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
        picture: str = payload.get("picture")

        if id is None:
            raise credentials_exeption
        token_data = schemas.TokenData(id=id, account_type=account_type, picture=picture)
    except JWTError:
        raise credentials_exeption
    
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exeption = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    return verify_access_token(token, credentials_exeption)


def validate_security_token(token, client_ids):
    # Get Google's RISC configuration.
    risc_config_uri = 'https://accounts.google.com/.well-known/risc-configuration'
    risc_config = requests.get(risc_config_uri).json()

    # Get the public key used to sign the token.
    google_certs = requests.get(risc_config['jwks_uri']).json()
    jwt_header = jwt.get_unverified_header(token)
    key_id = jwt_header['kid']
    public_key = None
    for key in google_certs['keys']:
        if key['kid'] == key_id:
            public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(key))
    if not public_key:
        # In this situation, return HTTP 400
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Public key certificate not found.")

    # Decode the token, validating its signature, audience, and issuer.
    try:
        token_data = jwt.decode(token, public_key, algorithms='RS256',
                                options={'verify_exp': False},
                                audience=client_ids, issuer=risc_config['issuer'])
    except:
        # Validation failed. Return HTTP 400.
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Validation failed.")
    return token_data