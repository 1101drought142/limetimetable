import datetime
from pydantic import BaseModel

import apps.timetable.models as db_models

class BaseScheme(BaseModel):
    class Config:
        arbitrary_types_allowed = True

class AddOrderScheme(BaseScheme):
    start_time: str
    end_time: str
    clients: list
    corts: list
    cort: int
    colors: list

class GetChangeModalScheme(BaseScheme):
    start_time: str
    end_time: str
    order: db_models.Order
    clients: list
    corts: list
    client: db_models.Client
    colors: list

class AddRepeatativeBlockScheme(BaseScheme):
    corts: list
    weekdays: list
    cort: int
    colors: list

class GetChangeModalRepeatativeScheme(BaseScheme):
    start_time: str
    end_time: str
    repeatative_order: db_models.TypicalRaspisanieObject
    corts: list
    weekdays: list
    curent_weekdays: list
    colors: list


class ValidatedOrderObject(BaseScheme):
    date: datetime.date
    starttime: datetime.time
    endtime: datetime.time
    payed: bool
    name: str
    phone: str
    mail: str
    bitrix_id: str
    site_id: str|None
    cort_id: int    
    block_id: int|None

class ValidatedRepeatativeOrderObject(BaseScheme):
    starttime: datetime.time
    endtime: datetime.time
    description: str
    weekdays: str
    cort_id: int
    block_id: int|None

class TableScheme(BaseScheme):
    data: list
    timerange: list


class ApiOrder(BaseScheme):
    date: datetime.date
    timedata: dict