from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from apps.timetable import models as timetable_models
from apps.timetable.routes import router as timetable_routes

from apps.users import models as users_models
from apps.users.routes import router as users_routes

from database import engine

timetable_models.Base.metadata.create_all(bind=engine)
users_models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age = -1,
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(timetable_routes)
app.include_router(users_routes)