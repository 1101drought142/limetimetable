from abc import abstractmethod
import datetime
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from logic.validators import OrderValidator
from logic.utils import get_order_object, delete_order_object, get_clients

def datetime_picker_format(date : datetime.datetime):
    return date.strftime("%d-%m-%Y %H:%M")

class GenerateModalHTML(BaseModel):
    @abstractmethod
    def return_html_template():
      raise NotImplemented()

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

    def validate_data_and_do_sql(self):
        start_time = datetime.datetime.strptime(self.date_start, '%d-%m-%Y %H:%M')
        end_time = datetime.datetime.strptime(self.date_end, '%d-%m-%Y %H:%M')
        try:
            validator = OrderValidator(self.client_name, self.client_phone, self.client_mail, self.status, start_time.time(), end_time.time(), start_time.date(), self.client_bitrix_id, self.client_site_id, None)
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

    def validate_data_and_do_sql(self):
        start_time = datetime.datetime.strptime(self.date_start, '%d-%m-%Y %H:%M')
        end_time = datetime.datetime.strptime(self.date_end, '%d-%m-%Y %H:%M')
        try:
            validator = OrderValidator(self.client_name, self.client_phone, self.client_mail, self.status, start_time.time(), end_time.time(), start_time.date(), self.client_bitrix_id, self.client_site_id, int(self.block_id))
            if (validator.validate()): validator.update_object()
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