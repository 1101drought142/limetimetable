from abc import abstractmethod
import datetime
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from logic.validators import OrderValidator
from logic.utils import get_order_object, delete_order_object

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
        })
    
class GetChangeModalTemplate(BaseModel):
    block_id : str
    def return_html_template(self, request, templates):
        order_object = get_order_object(int(self.block_id))
        date = order_object[0].date
        start_timeinterval = order_object[1].time_object
        end_timeinterval = order_object[2].time_object
        start_time = datetime.datetime(year=date.year, month=date.month, day=date.day, hour=start_timeinterval.hour, minute=start_timeinterval.minute)
        end_time = datetime.datetime(year=date.year, month=date.month, day=date.day, hour=end_timeinterval.hour, minute=end_timeinterval.minute)


        return templates.TemplateResponse("change_block_modal.html", {
            "request": request, 
            "start_time" :  datetime_picker_format(start_time),
            "end_time" : datetime_picker_format(end_time),
            "order": order_object[0],
        })
    
class CreateNewTimeBlockTemplate(BaseModel):
    date_start: str
    date_end: str
    status: str

    def validate_data_and_do_sql(self):
        start_time = datetime.datetime.strptime(self.date_start, '%d-%m-%Y %H:%M')
        end_time = datetime.datetime.strptime(self.date_end, '%d-%m-%Y %H:%M')
        try:
            OrderValidator("Иван", "8 983 313-70-82", start_time.time(), end_time.time(), start_time.date()).validate_and_create()
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