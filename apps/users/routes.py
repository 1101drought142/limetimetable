# @router.post("/login")
# def login(user: dict = Depends(authenticate_user)):
#     session_id = create_session(user["user_id"])
#     return {"message": "Logged in successfully", "session_id": session_id}
from typing import Annotated

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

import apps.users.queries as user_queries
import apps.users.models as user_models
from apps.users.logic import isadmin
from database import get_db

router = APIRouter(prefix='/user', tags=['users'])
templates = Jinja2Templates(directory="templates")

@router.get("/logs", response_class=HTMLResponse)
def logs(request: Request, user: Annotated[user_models.User, Depends(isadmin)], db: Session = Depends(get_db)):
    logs = user_queries.get_logs(db)
    return templates.TemplateResponse("userlog.html", {"request": request, "logs" : logs})
