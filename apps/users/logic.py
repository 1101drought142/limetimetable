import random 

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import RedirectResponse

import apps.users.queries as user_queries
from database import get_db

security = HTTPBasic()

def authenticate_user(credentials: HTTPBasicCredentials = Depends(security), db = Depends(get_db)):
    user = user_queries.get_user_or_None(db, credentials.username, credentials.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user

def isadmin(user = Depends(authenticate_user)):
    return user.is_admin()