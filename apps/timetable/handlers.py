from pydantic import BaseModel

class GetAddNewBlockModalTemplate(BaseModel):
    start_time : str
    date: str
    
class GetChangeModalTemplate(BaseModel):
    block_id : str
    
class GetChangeModalRepeatativeTemplate(BaseModel):
    block_id : str

class CreateNewTimeBlockTemplate(BaseModel):
    date_start: str
    date_end: str
    status: bool
    client_name: str
    client_phone: str
    client_mail: str
    client_bitrix_id: str
    client_site_id: str
    cort_id: str

class ChangeTimeBlockTemplate(BaseModel):
    block_id: str
    date_start: str
    date_end: str
    status: bool
    client_name: str
    client_phone: str
    client_mail: str
    client_bitrix_id: str
    client_site_id: str
    cort_id: str

class ChangeRepeatativeTimeBlockTemplate(BaseModel):
    block_id: str
    time_start: str
    time_end: str
    description: str
    days: list
    cort_id: str

class CreateNewRepeatativeTimeBlockTemplate(BaseModel):
    time_start: str
    time_end: str
    description: str
    days: list
    cort_id: str

class DeleteTimeBlockTemplate(BaseModel):
    block_id: str

class DeleteRepeatativeTimeBlockTemplate(BaseModel):
    block_id: str

class GetFilteredTable(BaseModel):
    date_range: str
    cort_id: str