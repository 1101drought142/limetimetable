from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from logic.datelogic import DateLogic
from database import Order
from logic.request_handlers import GetAddNewBlockModalTemplate, CreateNewTimeBlockTemplate, GetChangeModalTemplate, DeleteTimeBlockTemplate, ChangeTimeBlockTemplate, GetFilteredTable, GetAddNewRepeatativeBlockModalTemplate, CreateNewRepeatativeTimeBlockTemplate, GetChangeModalTemplate, ChangeRepeatativeTimeBlockTemplate, GetChangeModalRepeatativeTemplate, DeleteRepeatativeTimeBlockTemplate
from logic.websockets_connection import ConnectionManager
from logic.utils import get_corts

templates = Jinja2Templates(directory="templates")
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
manager = ConnectionManager()


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    data = DateLogic().create_date_data(cort_id=1)
    corts = get_corts()
    return templates.TemplateResponse("index.html", {"request": request, "data": data, "time_range" : DateLogic().get_date_interval(), "corts": corts})

@app.websocket("/ws/{client_id}")
async def websocket_endpoint( websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.post("/api/server/v1/renew_table/", response_class=HTMLResponse)
def get_time_table (request: Request, request_data: GetFilteredTable):
    return  request_data.return_html_template(request, templates)

@app.post("/api/server/v1/get_create_modal_template/", response_class=HTMLResponse)
def create_modal(request: Request, request_data: GetAddNewBlockModalTemplate):
    return request_data.return_html_template(request, templates)

@app.post("/api/server/v1/get_change_modal_template/", response_class=HTMLResponse)
def change_modal(request: Request, request_data: GetChangeModalTemplate):
    return request_data.return_html_template(request, templates)


@app.post("/api/server/v1/get_create_repeatative_modal_template/", response_class=HTMLResponse)
def create_repeatative_modal(request: Request, request_data: GetAddNewRepeatativeBlockModalTemplate):
    return request_data.return_html_template(request, templates)

@app.post("/api/server/v1/get_change_repeatative_modal_template/", response_class=HTMLResponse)
def create_repeatative_modal(request: Request, request_data: GetChangeModalRepeatativeTemplate):
    return request_data.return_html_template(request, templates)

@app.post("/api/server/v1/create_raspisanie_object/", response_class=JSONResponse)
async def create_modal(request: Request, request_data: CreateNewTimeBlockTemplate):
    creation_result = request_data.validate_data_and_do_sql()
    if (creation_result == True):
        await manager.broadcast_html( "renew" )
        return JSONResponse(content=jsonable_encoder({"success": True}), status_code=201)
    else:    
        return JSONResponse(content=jsonable_encoder({"success": False, "error": str(creation_result), }), status_code=422)

@app.post("/api/server/v1/delete_raspisanie_object/", response_class=JSONResponse)
async def delete_modal(request: Request, request_data: DeleteTimeBlockTemplate):
    creation_result = request_data.validate_data_and_do_sql()
    if (creation_result == True):
        await manager.broadcast_html("renew")
        return JSONResponse(content=jsonable_encoder({"success": True}), status_code=201)
    else:    
        return JSONResponse(content=jsonable_encoder({"success": False, "error": str(creation_result), }), status_code=422)    

@app.post("/api/server/v1/change_raspisanie_object/", response_class=JSONResponse)
async def update_modal(request: Request, request_data: ChangeTimeBlockTemplate):
    creation_result = request_data.validate_data_and_do_sql()
    if (creation_result == True):
        await manager.broadcast_html("renew")
        return JSONResponse(content=jsonable_encoder({"success": True}), status_code=201)
    else:    
        return JSONResponse(content=jsonable_encoder({"success": False, "error": str(creation_result), }), status_code=422)
    

@app.post("/api/server/v1/create_repeatative_raspisanie_object/", response_class=JSONResponse)
async def create_repeatative_modal(request: Request, request_data: CreateNewRepeatativeTimeBlockTemplate):
    creation_result = request_data.validate_data_and_do_sql()
    if (creation_result == True):
        await manager.broadcast_html( "renew" )
        return JSONResponse(content=jsonable_encoder({"success": True}), status_code=201)
    else:    
        return JSONResponse(content=jsonable_encoder({"success": False, "error": str(creation_result), }), status_code=422)
    
@app.post("/api/server/v1/change_repeatative_raspisanie_object/", response_class=JSONResponse)
async def update_modal(request: Request, request_data: ChangeRepeatativeTimeBlockTemplate):
    creation_result = request_data.validate_data_and_do_sql()
    if (creation_result == True):
        await manager.broadcast_html("renew")
        return JSONResponse(content=jsonable_encoder({"success": True}), status_code=201)
    else:    
        return JSONResponse(content=jsonable_encoder({"success": False, "error": str(creation_result), }), status_code=422)
    
@app.post("/api/server/v1/delete_repeatative_raspisanie_object/", response_class=JSONResponse)
async def delete_modal(request: Request, request_data: DeleteRepeatativeTimeBlockTemplate):
    creation_result = request_data.validate_data_and_do_sql()
    if (creation_result == True):
        await manager.broadcast_html("renew")
        return JSONResponse(content=jsonable_encoder({"success": True}), status_code=201)
    else:    
        return JSONResponse(content=jsonable_encoder({"success": False, "error": str(creation_result), }), status_code=422)    
    

# @app.get("/api/v1/order_time/", response_class=JSONResponse)
# async def get_available_time(request: Request, request_data: GetAvailableTime):
#     pass

# @app.post("/api/v1/order/", response_class=JSONResponse)
# async def api_create_object(request: Request, request_data: CreateObjectApi):
#     pass

# @app.post("/api/v1/order_payed/", response_class=JSONResponse)
# async def api_update_object_payed(request: Request, request_data: UpdateObjectPayedApi):
#     pass
