from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from database import SessionLocal, init_db
templates = Jinja2Templates(directory="templates")

time_range = [
    "10-11",
    "11-12",
    "12-13",
]

fake_data = [
    {
        "day" : "test day 1",
        "date" : "10.10",
        "time" : [  
            {
                "status" : "empty",    
                "test" : "1_1",  
                "rowspan": 3,
            },
            {
                "status" : "ordered",
                "test" : "1_1",
                "hide" : True,    
            },
            {
                "status" : "empty",
                "test" : "1_1",  
                "hide" : True,
            }
        ]
    }, 
    {
        "day" : "test day 2",
        "date" : "10.10",
        "time" : [  
            {
                "status" : "empty",
                "test" : "2_1",
            },
            {
                "status" : "ordered",
                "test" : "2_2",  
            },
            {
                "status" : "empty",
                "test" : "2_3",  
            }
        ]
    }
]


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("table.html", {"request": request, "data": fake_data, "time_range" : time_range})
