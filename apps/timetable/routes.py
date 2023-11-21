from fastapi import  Request, APIRouter, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import timetable.queries as db_query 
import timetable.handlers as handlers
from timetable.logic import DateLogic
from timetable.websockets_connection import ConnectionManager
from database import get_db

router = APIRouter(prefix='/', tags=['User'])
templates = Jinja2Templates(directory="templates")
manager = ConnectionManager()

#user: Annotated[User, Depends(manager_restriction)]

@router.get("/", response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(get_db)):
    data = DateLogic.create_date_data(db, cort_id=1)
    corts = db_query.get_corts(db)
    return templates.TemplateResponse("index.html", {"request": request, "data": data, "time_range" : db_query.get_intervals(db), "corts": corts})

@router.post("/api/server/v1/renew_table/", response_class=HTMLResponse)
def get_time_table (request: Request, request_data: handlers.GetFilteredTable):
    return  request_data.return_html_template(request, templates)

@router.post("/api/server/v1/get_create_modal_template/", response_class=HTMLResponse)
def create_modal(request: Request, request_data: handlers.GetAddNewBlockModalTemplate):
    return request_data.return_html_template(request, templates)

@router.post("/api/server/v1/get_change_modal_template/", response_class=HTMLResponse)
def change_modal(request: Request, request_data: handlers.GetChangeModalTemplate):
    return request_data.return_html_template(request, templates)


@router.post("/api/server/v1/get_create_repeatative_modal_template/", response_class=HTMLResponse)
def create_repeatative_modal(request: Request, request_data: handlers.GetAddNewRepeatativeBlockModalTemplate):
    return request_data.return_html_template(request, templates)

@router.post("/api/server/v1/get_change_repeatative_modal_template/", response_class=HTMLResponse)
def create_repeatative_modal(request: Request, request_data: handlers.GetChangeModalRepeatativeTemplate):
    return request_data.return_html_template(request, templates)

@router.post("/api/server/v1/create_raspisanie_object/", response_class=JSONResponse)
async def create_modal(request: Request, request_data: handlers.CreateNewTimeBlockTemplate):
    creation_result = request_data.validate_data_and_do_sql()
    if (creation_result == True):
        await manager.broadcast_html( "renew" )
        return JSONResponse(content=jsonable_encoder({"success": True}), status_code=201)
    else:    
        return JSONResponse(content=jsonable_encoder({"success": False, "error": str(creation_result), }), status_code=422)

@router.post("/api/server/v1/delete_raspisanie_object/", response_class=JSONResponse)
async def delete_modal(request: Request, request_data: handlers.DeleteTimeBlockTemplate):
    creation_result = request_data.validate_data_and_do_sql()
    if (creation_result == True):
        await manager.broadcast_html("renew")
        return JSONResponse(content=jsonable_encoder({"success": True}), status_code=201)
    else:    
        return JSONResponse(content=jsonable_encoder({"success": False, "error": str(creation_result), }), status_code=422)    

@router.post("/api/server/v1/change_raspisanie_object/", response_class=JSONResponse)
async def update_modal(request: Request, request_data: handlers.ChangeTimeBlockTemplate):
    creation_result = request_data.validate_data_and_do_sql()
    if (creation_result == True):
        await manager.broadcast_html("renew")
        return JSONResponse(content=jsonable_encoder({"success": True}), status_code=201)
    else:    
        return JSONResponse(content=jsonable_encoder({"success": False, "error": str(creation_result), }), status_code=422)
    

@router.post("/api/server/v1/create_repeatative_raspisanie_object/", response_class=JSONResponse)
async def create_repeatative_modal(request: Request, request_data: handlers.CreateNewRepeatativeTimeBlockTemplate):
    creation_result = request_data.validate_data_and_do_sql()
    if (creation_result == True):
        await manager.broadcast_html( "renew" )
        return JSONResponse(content=jsonable_encoder({"success": True}), status_code=201)
    else:    
        return JSONResponse(content=jsonable_encoder({"success": False, "error": str(creation_result), }), status_code=422)
    
@router.post("/api/server/v1/change_repeatative_raspisanie_object/", response_class=JSONResponse)
async def update_modal(request: Request, request_data: handlers.ChangeRepeatativeTimeBlockTemplate):
    creation_result = request_data.validate_data_and_do_sql()
    if (creation_result == True):
        await manager.broadcast_html("renew")
        return JSONResponse(content=jsonable_encoder({"success": True}), status_code=201)
    else:    
        return JSONResponse(content=jsonable_encoder({"success": False, "error": str(creation_result), }), status_code=422)
    
@router.post("/api/server/v1/delete_repeatative_raspisanie_object/", response_class=JSONResponse)
async def delete_modal(request: Request, request_data: handlers.DeleteRepeatativeTimeBlockTemplate):
    creation_result = request_data.validate_data_and_do_sql()
    if (creation_result == True):
        await manager.broadcast_html("renew")
        return JSONResponse(content=jsonable_encoder({"success": True}), status_code=201)
    else:    
        return JSONResponse(content=jsonable_encoder({"success": False, "error": str(creation_result), }), status_code=422)    
    