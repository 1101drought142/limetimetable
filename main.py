from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from datelogic import DateLogic
from database import Order
from request_handlers import GetAddNewBlockModalTemplate, CreateNewTimeBlockTemplate
from websockets_connection import ConnectionManager

templates = Jinja2Templates(directory="templates")
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
manager = ConnectionManager()

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    data = DateLogic().create_date_data()
    return templates.TemplateResponse("index.html", {"request": request, "data": data, "time_range" : DateLogic().get_date_interval()})

@app.websocket("/ws")
async def websocket_endpoint(request: Request, websocket: WebSocket):
    await manager.accept(websocket)
    while True:
        data = DateLogic().create_date_data()
        return templates.TemplateResponse("table.html", {"request": request, "data": data, "time_range" : DateLogic().get_date_interval()})

@app.get("/api/server/v1/renew_table/", response_class=HTMLResponse)
def get_time_table (request: Request):
    pass

@app.post("/api/server/v1/get_create_modal_template/", response_class=HTMLResponse)
def create_modal(request: Request, request_data: GetAddNewBlockModalTemplate):
    return request_data.return_html_template(request, templates)

@app.post("/api/server/v1/create_raspisanie_object/", response_class=HTMLResponse)
def create_modal(request: Request, request_data: CreateNewTimeBlockTemplate):
    creation_result = request_data.validate_data_and_create_model()
    if (creation_result == True):

        return JSONResponse(content=jsonable_encoder({"success": True}), status_code=201)
        
    else:    
        return JSONResponse(content=jsonable_encoder({"success": False, "error": str(creation_result), }), status_code=422)