from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from datelogic import DateLogic
templates = Jinja2Templates(directory="templates")
data = DateLogic().create_date_data()
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("table.html", {"request": request, "data": data, "time_range" : DateLogic().get_date_interval()})


@app.get("/renew_table/", response_class=HTMLResponse)
def get_time_table (request: Request):
    return templates.TemplateResponse("table.html", {"request": request, "data": data, "time_range" : DateLogic().get_date_interval()})
