# @router.post("/login")
# def login(user: dict = Depends(authenticate_user)):
#     session_id = create_session(user["user_id"])
#     return {"message": "Logged in successfully", "session_id": session_id}
from fastapi import APIRouter, Depends, HTTPException, status

import apps.users.logic as user_logic
router = APIRouter(prefix='/user', tags=['timetable'])

@router.post("/logout")
def logout(session_id: int = Depends(user_logic.get_session_id)):
    if session_id not in sessions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    sessions.pop(session_id)
    return {"message": "Logged out successfully", "session_id": session_id}