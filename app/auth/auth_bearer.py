#The goal of this file is to check whether the reques tis authorized or not [ verification of the proteced route]
import sys
sys.path.append(sys.path[0] + "/app/auth")
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .auth_handler import decodeJWT
from app.aws.aws_controller import get_token_by_id

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        #checks for authorization header
        auth_cookie = request.cookies.get("Authorization")
        if auth_cookie == None:
            raise HTTPException(status_code=403, detail="no token.")
        else:
            token = auth_cookie.split("Bearer ")[1]
            credentials = {'scheme': "Bearer", 'credentials': token}
            print('req : ',credentials)
            if credentials:
                if not credentials['scheme'] == "Bearer":
                    raise HTTPException(status_code=403, detail="Invalid authentication scheme." )
                if not self.verify_jwt(credentials['credentials']):
                    raise HTTPException(status_code=403, detail="Invalid token or expired token.")
                
                return credentials['credentials']
            else:
                raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = decodeJWT(jwtoken)
        except:
            payload = None
        if payload:
            db_token = get_token_by_id(payload['user_id'])
            print(db_token)
            isTokenValid = db_token == jwtoken
        return isTokenValid