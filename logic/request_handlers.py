from abc import abstractmethod
import datetime
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from logic.validators import OrderValidator, RepeatativeTaskValidator
from logic.utils import get_order_object, delete_order_object, get_clients, get_corts, get_repeatative_order_object, delete_repatative_order_object
from logic.datelogic import DateLogic
from database import Weekday, DataBaseFormatedWeekday

def datetime_picker_format(date : datetime.datetime):
    return date.strftime("%d-%m-%Y %H:%M")

def time_picker_format(date : datetime.time):
    return date.strftime("%H:%M")

class GetAddNewBlockModalTemplate(BaseModel):
    start_time : str
    date: str
    def return_html_template(self, request, templates):
        start_time = datetime.datetime.fromisoformat(f"{self.date} {self.start_time}") 
        end_time = start_time + datetime.timedelta(hours=1)
        return templates.TemplateResponse("add_new_block_modal.html", {
            "request": request, 
            "start_time" :  datetime_picker_format(start_time),
            "end_time" : datetime_picker_format(end_time),
            "clients": get_clients(),
            "corts" : get_corts(),
        })
    
class GetChangeModalTemplate(BaseModel):
    block_id : str
    def return_html_template(self, request, templates):
        order_object = get_order_object(int(self.block_id))
        order, start_time_db, end_time_db, client = order_object

        date = order.date
        start_timeinterval = start_time_db.time_object
        end_timeinterval = end_time_db.time_object
        start_time = datetime.datetime(year=date.year, month=date.month, day=date.day, hour=start_timeinterval.hour, minute=start_timeinterval.minute)
        end_time = datetime.datetime(year=date.year, month=date.month, day=date.day, hour=end_timeinterval.hour, minute=end_timeinterval.minute)


        return templates.TemplateResponse("change_block_modal.html", {
            "request": request, 
            "start_time" :  datetime_picker_format(start_time),
            "end_time" : datetime_picker_format(end_time),
            "order": order,
            "clients": get_clients(),
            "client" : client,
            "corts" : get_corts(),
        })

class GetAddNewRepeatativeBlockModalTemplate(BaseModel):

    def return_html_template(self, request, templates):
        return templates.TemplateResponse("add_new_repeatative_task_modal.html", {
            "request": request, 
            "corts" : get_corts(),
            "weekdays": [e for e in Weekday],
        })
    
class GetChangeModalRepeatativeTemplate(BaseModel):
    block_id : str
    def return_html_template(self, request, templates):
        repeatative_order_object = get_repeatative_order_object(int(self.block_id))
        repeatative_order, start_time_db, end_time_db = repeatative_order_object

        start_timeinterval = start_time_db.time_object
        end_timeinterval = end_time_db.time_object
        start_time = datetime.time(hour=start_timeinterval.hour, minute=start_timeinterval.minute)
        end_time = datetime.time(hour=end_timeinterval.hour, minute=end_timeinterval.minute)


        return templates.TemplateResponse("change_repeatative_task_modal.html", {
            "request": request, 
            "start_time" :  time_picker_format(start_time),
            "end_time" : time_picker_format(end_time),
            "repeatative_order": repeatative_order,
            "corts" : get_corts(),
            "weekdays": [e for e in Weekday],
            "curent_weekdays": DataBaseFormatedWeekday.format_from_string(repeatative_order.weekdays)
        })
    

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
    def validate_data_and_do_sql(self):
        start_time = datetime.datetime.strptime(self.date_start, '%d-%m-%Y %H:%M')
        end_time = datetime.datetime.strptime(self.date_end, '%d-%m-%Y %H:%M')
        try:
            validator = OrderValidator(self.client_name, self.client_phone, self.client_mail, self.status, start_time.time(), end_time.time(), start_time.date(), self.client_bitrix_id, self.client_site_id, None, self.cort_id)
            if (validator.validate()): validator.create_object()
        except Exception as ex:
            return ex
        return True

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
    def validate_data_and_do_sql(self):
        start_time = datetime.datetime.strptime(self.date_start, '%d-%m-%Y %H:%M').time()
        end_time = datetime.datetime.strptime(self.date_end, '%d-%m-%Y %H:%M').time()
        try:
            validator = OrderValidator(self.client_name, self.client_phone, self.client_mail, self.status, start_time.time(), end_time.time(), start_time.date(), self.client_bitrix_id, self.client_site_id, int(self.block_id), self.cort_id)
            if (validator.validate()): validator.update_object()
        except Exception as ex:
            return ex
        return True

class ChangeRepeatativeTimeBlockTemplate(BaseModel):
    block_id: str
    time_start: str
    time_end: str
    description: str
    days: list
    cort_id: str
    def validate_data_and_do_sql(self):
        try:
            validator = RepeatativeTaskValidator(self.time_start, self.time_end, self.description, self.days, self.cort_id, self.block_id)
            if (validator.validate()): validator.update_object()
        except Exception as ex:
            return ex
        return True

class CreateNewRepeatativeTimeBlockTemplate(BaseModel):
    time_start: str
    time_end: str
    description: str
    days: list
    cort_id: str
    def validate_data_and_do_sql(self):
        try:
            validator = RepeatativeTaskValidator(self.time_start, self.time_end, self.description, self.days, self.cort_id)
            if (validator.validate()): validator.create_object()
        except Exception as ex:
            return ex
        return True

class DeleteTimeBlockTemplate(BaseModel):
    block_id: str
    def validate_data_and_do_sql(self):
        try:
            delete_order_object(int(self.block_id))
        except Exception as ex:
            return ex
        return True

class DeleteRepeatativeTimeBlockTemplate(BaseModel):
    block_id: str
    def validate_data_and_do_sql(self):
        try:
            delete_repatative_order_object(int(self.block_id))
        except Exception as ex:
            return ex
        return True

class GetFilteredTable(BaseModel):
    date_range: str
    cort_id: str
    def return_html_template(self, request, templates):
        if (self.date_range):
            start_date_str, end_date_str = self.date_range.replace(" ", "").split("-")
            start_date = datetime.datetime.strptime(start_date_str,'%d.%m.%Y').date()
            end_date = datetime.datetime.strptime(end_date_str, '%d.%m.%Y').date()
        else:
            start_date = end_date = None

        cort_id = 1
        if (self.cort_id):
            cort_id = self.cort_id
        data = DateLogic().create_date_data(start_date, end_date, cort_id)
        return templates.TemplateResponse("table.html", {"request": request, "data": data, "time_range" : DateLogic().get_date_interval()})
    