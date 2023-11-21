# @router.post("/login")
# def login(user: dict = Depends(authenticate_user)):
#     session_id = create_session(user["user_id"])
#     return {"message": "Logged in successfully", "session_id": session_id}
from fastapi import APIRouter, Depends, HTTPException, status

import apps.users.logic as user_logic
router = APIRouter(prefix='/user', tags=['timetable'])

@router.post("/logout")
def logout():
    pass