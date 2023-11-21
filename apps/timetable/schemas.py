import datetime
from pydantic import BaseModel

import apps.timetable.models as db_models

class BaseScheme(BaseModel):
    class Config:
        arbitrary_types_allowed = True
        orm_mode = True

class AddOrderScheme(BaseScheme):
    start_time: datetime.datetime
    end_time: datetime.datetime
    clients: list
    corts: list

class GetChangeModalScheme(BaseScheme):
    start_time: datetime.datetime
    end_time: datetime.datetime
    order: db_models.Order
    clients: list
    corts: list
    client: db_models.Client

class AddRepeatativeBlockScheme(BaseScheme):
    corts: list
    weekdays: list

class GetChangeModalRepeatativeScheme(BaseScheme):
    start_time: datetime.datetime
    end_time: datetime.datetime
    repeatative_order: db_models.TypicalRaspisanieObject
    corts: list
    weekdays: list
    curent_weekdays: list


class ValidatedOrderObject(BaseScheme):
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