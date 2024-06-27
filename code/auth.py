import os
from datetime import datetime, timedelta
import jwt
from fastapi import Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def generate_secret_key():
    return os.urandom(24).hex()

SECRET_KEY = generate_secret_key()

# генерация JWT
def create_jwt(user_data):
    exp_time = datetime.utcnow() + timedelta(hours=6)
    payload = {
        "user_id": user_data.id,
        "role": user_data.role,
        "exp": int(exp_time.timestamp())
    }
    jwt_token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return jwt_token

# проверка JWT
def verify_jwt(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

class User(BaseModel):
    id: int
    role: str

async def get_current_user(request: Request):
    token = request.cookies.get("jwe_token")
    if not token:
        # Можно сразу же вернуть редирект или JSON
        return RedirectResponse(url="/")
    token = token.replace("Bearer ", "")
    try:
        payload = verify_jwt(token)
    except jwt.ExpiredSignatureError:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": "Token expired", "redirect": "/"})
    except jwt.InvalidTokenError:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": "Invalid token", "redirect": "/"})
    return User(id=payload["user_id"], role=payload["role"])


# словарь доступа роута по роли
access_control = {
    "/": ["public"],
    "/menu": ["all"],
    "/welcome": ["all"],
    "/board": ["all"],
    "/token": ["public"],
    "/register": ['public'],
    "/favicon.ico": ['public'],
    "/reg": ['public'],
    "/man": ["root"],
    "/a": ["help","root"]
    "/b": ["user","root"]
}