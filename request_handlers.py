from abc import abstractmethod
import datetime
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates

def datetime_picker_format(date : datetime.datetime):
    return date.strftime("%d-%m-%Y %H:%M")

class GenerateModalHTML(BaseModel):
    @abstractmethod
    def return_html_template():
      return None

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