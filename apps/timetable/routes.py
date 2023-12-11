from fastapi import  Request, APIRouter, Depends, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Annotated

import apps.timetable.queries as db_query 
import apps.timetable.handlers as handlers
from apps.timetable.logic import DateLogic, tg_raspisanie_alert
from apps.timetable.websockets_connection import ConnectionManager
from apps.users.logic import authenticate_user
from apps.users.models import User
from apps.users.queries import create_log

from database import get_db

router = APIRouter(prefix='', tags=['timetable'])
templates = Jinja2Templates(directory="templates")
manager = ConnectionManager()

@router.get("/", response_class=HTMLResponse)
def index(request: Request, user: Annotated[User, Depends(authenticate_user)] , db: Session = Depends(get_db)):
    data = DateLogic().create_date_data(db, cort_id=1)
    corts = db_query.get_corts(db)
    return templates.TemplateResponse("index.html", {"request": request, "data": data, "time_range" : db_query.get_intervals(db), "corts": corts, "user": user})

@router.websocket("/ws/{client_id}")
async def websocket_endpoint( websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@router.post("/api/server/v1/renew_table/", response_class=HTMLResponse)
def get_time_table (request: Request, user: Annotated[User, Depends(authenticate_user)] , request_data: handlers.GetFilteredTable, db: Session = Depends(get_db)):
    request_data_result = request_data.get_validated_result(db=db)
    return templates.TemplateResponse("table.html", {"request": request, "data": request_data_result.data, "time_range" : request_data_result.timerange})


@router.post("/api/server/v1/get_create_modal_template/", response_class=HTMLResponse)
def create_modal(request: Request, user: Annotated[User, Depends(authenticate_user)], request_data: handlers.GetAddOrderTemplateHandler, db: Session = Depends(get_db)):
    request_data_result = request_data.get_validated_result(db=db)
    return templates.TemplateResponse("add_new_block_modal.html", {
        "request": request, 
        "start_time" :  request_data_result.start_time,
        "end_time" : request_data_result.end_time,
        "clients": request_data_result.clients,
        "corts" : request_data_result.corts,
        "cort" : request_data.cort,
    })

@router.post("/api/server/v1/get_change_modal_template/", response_class=HTMLResponse)
def change_modal(request: Request , user: Annotated[User, Depends(authenticate_user)] , request_data: handlers.GetChangeModalTemplateHandler, db: Session = Depends(get_db)):
    request_data_result = request_data.get_validated_result(db=db)
    return templates.TemplateResponse("change_block_modal.html", {
        "request": request, 
        "start_time" :  request_data_result.start_time,
        "end_time" : request_data_result.end_time,
        "order": request_data_result.order,
        "clients": request_data_result.clients,
        "client" : request_data_result.client,
        "corts" : request_data_result.corts,
    })


@router.post("/api/server/v1/get_create_repeatative_modal_template/", response_class=HTMLResponse)
def create_repeatative_modal(request: Request , user: Annotated[User, Depends(authenticate_user)] , request_data: handlers.GetAddRepeatativeBlockModalTemplate, db: Session = Depends(get_db)):
    request_data_result = request_data.get_validated_result(db=db)
    return templates.TemplateResponse("add_new_repeatative_task_modal.html", {
        "request": request, 
        "corts" : request_data_result.corts,
        "weekdays": request_data_result.weekdays,
    })

@router.post("/api/server/v1/get_change_repeatative_modal_template/", response_class=HTMLResponse)
def change_repeatative_modal(request: Request , user: Annotated[User, Depends(authenticate_user)] , request_data: handlers.GetChangeModalRepeatativeTemplateHandler, db: Session = Depends(get_db)):
    request_data_result = request_data.get_validated_result(db=db)
    return templates.TemplateResponse("change_repeatative_task_modal.html", {
        "request": request, 
        "start_time" :  request_data_result.start_time,
        "end_time" : request_data_result.end_time,
        "repeatative_order": request_data_result.repeatative_order,
        "corts" : request_data_result.corts,
        "weekdays": request_data_result.weekdays,
        "curent_weekdays": request_data_result.curent_weekdays,
    })

@router.post("/api/server/v1/create_raspisanie_object/", response_class=JSONResponse)
async def create_modal(request: Request , user: Annotated[User, Depends(authenticate_user)] , request_data: handlers.CreateNewTimeBlock, db: Session = Depends(get_db)):
    creation_result = request_data.execute_query(db)
    if (creation_result == True):
        create_log(db, user.id, "Создан новый блок расписания на " + " с " + str(request_data.date_start) + " по " + str(request_data.date_end) + " на корте " + str(request_data.cort_id) + " с оплатой " + str(request_data.status))
        await manager.broadcast_html( "renew" )
        return JSONResponse(content=jsonable_encoder({"success": True}), status_code=201)
    else:    
        return JSONResponse(content=jsonable_encoder({"success": False, "error": str(creation_result), }), status_code=422)

@router.post("/api/server/v1/delete_raspisanie_object/", response_class=JSONResponse)
async def delete_modal(request: Request , user: Annotated[User, Depends(authenticate_user)] , request_data: handlers.DeleteTimeBlock, db: Session = Depends(get_db)):
    creation_result = request_data.execute_query(db)
    if (creation_result == True):
        create_log(db, user.id, "Удален блок расписания с id" + str(request_data.block_id)) 
        await manager.broadcast_html("renew")
        return JSONResponse(content=jsonable_encoder({"success": True}), status_code=201)
    else:    
        return JSONResponse(content=jsonable_encoder({"success": False, "error": str(creation_result), }), status_code=422)    

@router.post("/api/server/v1/change_raspisanie_object/", response_class=JSONResponse)
async def update_modal(request: Request , user: Annotated[User, Depends(authenticate_user)] , request_data: handlers.ChangeTimeBlock, db: Session = Depends(get_db)):
    creation_result = request_data.execute_query(db)
    if (creation_result == True):
        create_log(db, user.id, "Обновлен блок расписания на " + " с " + str(request_data.date_start) + " по " + str(request_data.date_end) + " на корте " + str(request_data.cort_id) + " с оплатой " + str(request_data.status))
        await manager.broadcast_html("renew")
        return JSONResponse(content=jsonable_encoder({"success": True}), status_code=201)
    else:    
        return JSONResponse(content=jsonable_encoder({"success": False, "error": str(creation_result), }), status_code=422)
    

@router.post("/api/server/v1/create_repeatative_raspisanie_object/", response_class=JSONResponse)
async def create_repeatative(request: Request , user: Annotated[User, Depends(authenticate_user)] , request_data: handlers.CreateRepeatativeTimeBlock, db: Session = Depends(get_db)):
    creation_result = request_data.execute_query(db)
    if (creation_result == True):
        await manager.broadcast_html( "renew" )
        return JSONResponse(content=jsonable_encoder({"success": True}), status_code=201)
    else:    
        return JSONResponse(content=jsonable_encoder({"success": False, "error": str(creation_result), }), status_code=422)
    
@router.post("/api/server/v1/change_repeatative_raspisanie_object/", response_class=JSONResponse)
async def update_repeatative(request: Request, user: Annotated[User, Depends(authenticate_user)] , request_data: handlers.ChangeRepeatativeTimeBlock, db: Session = Depends(get_db)):
    creation_result = request_data.execute_query(db)
    if (creation_result == True):
        await manager.broadcast_html("renew")
        return JSONResponse(content=jsonable_encoder({"success": True}), status_code=201)
    else:    
        return JSONResponse(content=jsonable_encoder({"success": False, "error": str(creation_result), }), status_code=422)
    
@router.post("/api/server/v1/delete_repeatative_raspisanie_object/", response_class=JSONResponse)
async def delete_modal(request: Request, user: Annotated[User, Depends(authenticate_user)] , request_data: handlers.DeleteRepeatativeTimeBlock, db: Session = Depends(get_db)):
    creation_result = request_data.execute_query(db)
    if (creation_result == True):
        await manager.broadcast_html("renew")
        return JSONResponse(content=jsonable_encoder({"success": True}), status_code=201)
    else:    
        return JSONResponse(content=jsonable_encoder({"success": False, "error": str(creation_result), }), status_code=422)    

# @router.post("/api/v1/raspisanie", response_class=JSONResponse)
# async def get_raspisanie(request_data: handlers.GetRaspisanie, db: Session = Depends(get_db)):
#     creation_result = request_data.execute_query(db)
#     return JSONResponse(content=jsonable_encoder({"success": True, "data": creation_result}), status_code=200)

@router.get("/api/v1/raspisanie/{cort_id}/{date}/", response_class=JSONResponse)
async def get_raspisanie(cort_id, date, db: Session = Depends(get_db)):
    request_data =  handlers.GetRaspisanie(date, cort_id)
    creation_result = request_data.execute_query(db)
    return JSONResponse(content=jsonable_encoder({"success": True, "data": creation_result}), status_code=200)

@router.post("/api/v1/create_raspisanie", response_class=JSONResponse)
async def get_raspisanie(request_data: handlers.CreateNewTimeBlockBeforePayemnt, db: Session = Depends(get_db)):
    creation_result = request_data.execute_query(db)
    if (type(creation_result) == int):
        await manager.broadcast_html("renew")
        #tg_raspisanie_alert('Создан новый блок расписания, Дата: {creation_result.date}')
        return JSONResponse(content=jsonable_encoder({"success": True, "object_id": creation_result}), status_code=201)
    else:    
        return JSONResponse(content=jsonable_encoder({"success": False, "error": str(creation_result), }), status_code=422)


@router.post("/api/v1/set_paid_raspisanie", response_class=JSONResponse)
async def get_raspisanie(request_data: handlers.SetPayed, db: Session = Depends(get_db)):
    creation_result = request_data.execute_query(db)
    if (creation_result == True):
        await manager.broadcast_html("renew")
        return JSONResponse(content=jsonable_encoder({"success": True}), status_code=201)
    else:    
        return JSONResponse(content=jsonable_encoder({"success": False, "error": str(creation_result), }), status_code=422)
    
@router.post("/api/v1/get_links", response_class=JSONResponse)
async def get_translation_links(request_data: handlers.GetTranslationLinks, db: Session = Depends(get_db)):
    creation_result = request_data.execute_query(db)
    if (type(creation_result) == list):
        return JSONResponse(content=jsonable_encoder({"success": True, "links": creation_result}), status_code=201)
    else:    
        return JSONResponse(content=jsonable_encoder({"success": False, "error": str(creation_result), }), status_code=422)
