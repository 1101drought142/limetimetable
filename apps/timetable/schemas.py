import datetime
from pydantic import BaseModel

import timetable.models as db_models

class AddOrderScheme(BaseModel):
    start_time: datetime.datetime
    end_time: datetime.datetime
    clients: list
    corts: list

class GetChangeModalScheme(BaseModel):
    start_time: datetime.datetime
    end_time: datetime.datetime
    order: db_models.Order
    clients: list
    corts: list
    client: db_models.Client

class AddRepeatativeBlockScheme(BaseModel):
    corts: list
    weekdays: list

class GetChangeModalRepeatativeScheme(BaseModel):
    start_time: datetime.datetime
    end_time: datetime.datetime
    repeatative_order: db_models.TypicalRaspisanieObject
    corts: list
    weekdays: list
    curent_weekdays: list


class ValidatedOrderObject(BaseModel):
    date: datetime.date
    starttime: datetime.time
    endtime: datetime.time
    payed: bool
    name: str
    phone: str
    mail: str
    bitrix_id: str
    site_id: str
    cort_id: int    
    block_id: int|None

class ValidatedRepeatativeOrderObject(BaseModel):
    starttime: datetime.time
    endtime: datetime.time
    description: str
    weekdays: str
    cort_id: int
    block_id: int|None

class TableScheme(BaseModel):
    data: list
    timerange: list