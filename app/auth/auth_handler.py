# This file is responsible for signing , encoding , decoding and returning JWTS
import sys
sys.path.append(sys.path[0] + "/app/auth")
import time
from typing import Dict
import os

from dotenv import load_dotenv
import jwt

load_dotenv()
 
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")

def token_response(token: str):
    return {
        "access_token": token
    }

# function used for signing the JWT string
def signJWT(user_id: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM) 

    return token_response(token)


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {'user_id':None}
    

def validate_password(db_password: str, req_password: str) -> bool:

    return db_password == req_password

        
