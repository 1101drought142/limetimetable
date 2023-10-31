from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from datelogic import DateLogic
from request_handlers import GetAddNewBlockModalTemplate
templates = Jinja2Templates(directory="templates")
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    data = DateLogic().create_date_data()
    return templates.TemplateResponse("table.html", {"request": request, "data": data, "time_range" : DateLogic().get_date_interval()})

@app.get("/api/server/v1/renew_table/", response_class=HTMLResponse)
def get_time_table (request: Request):
    pass

@app.post("/api/server/v1/get_create_modal_template/", response_class=HTMLResponse)
def create_modal(request: Request, request_data: GetAddNewBlockModalTemplate):
    return request_data.return_html_template(request, templates)