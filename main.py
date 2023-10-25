from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from database import SessionLocal
from datelogic import DateLogic
templates = Jinja2Templates(directory="templates")

# fake_data = [
#     {
#         "day" : "test day 1",
#         "date" : "10.10",
#         "time" : [  
#             {
#                 "status" : "empty",    
#                 "test" : "1_1",  
#                 "rowspan": 3,
#             },
#             {
#                 "status" : "ordered",
#                 "test" : "1_1",
#                 "hide" : True,    
#             },
#             {
#                 "status" : "empty",
#                 "test" : "1_1",  
#                 "hide" : True,
#             }
#         ]
#     }, 
#     {
#         "day" : "test day 2",
#         "date" : "10.10",
#         "time" : [  
#             {
#                 "status" : "empty",
#                 "test" : "2_1",
#             },
#             {
#                 "status" : "ordered",
#                 "test" : "2_2",  
#             },
#             {
#                 "status" : "empty",
#                 "test" : "2_3",  
#             }
#         ]
#     }
# ]


data = DateLogic().create_date_data()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("table.html", {"request": request, "data": data, "time_range" : DateLogic().get_date_interval()})
