import random 

from fastapi import Request, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from main import sessions

import apps.users.queries as user_queries
def create_session(user_id: int):
    session_id = len(sessions) + random.randint(0, 1000000)
    sessions[session_id] = user_id
    return session_id

def get_session_id(request: Request):
    session_id = request.cookies.get("session_id")
    if session_id is None or int(session_id) not in sessions:
        raise HTTPException(status_code=401, detail="Invalid session ID")
    return int(session_id)

def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    if user_queries.get_user_or_None(credentials.username, credentials.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )