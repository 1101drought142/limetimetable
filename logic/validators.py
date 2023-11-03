import datetime
from sqlalchemy.orm import aliased

from database import session, Order, TimeIntervalObjects
from logic.utils import get_order_objects, create_new_object

class OrderValidator():
    def __init__(self, 
        name : str,
        phone : str,
        starttime: datetime.time,
        endtime: datetime.time,
        date: datetime.date
    ):
        self.name = name
        self.phone = phone
        self.starttime = starttime
        self.endtime = endtime
        self.date = date

    def validate_and_create(self) -> bool:
        if (self.starttime >= self.endtime):
            raise ValueError("Время окончания раньше времени начала")
        if (self.starttime < datetime.time(8, 0, 0) or self.endtime > datetime.time(23, 0, 0)):
            raise ValueError("Время не попадает в интервал работы корта")
       
        objects = get_order_objects()
        for object, starttime, endtime in objects:
            if (object.date == self.date):
                if not((self.starttime < starttime.time_object and self.endtime <= starttime.time_object) or (self.starttime >= endtime.time_object and self.endtime > endtime.time_object)):
                    raise ValueError("Время совпадает с занятым временем")
                
        if (create_new_object(self.date, self.starttime, self.endtime, False)):
            return True
        else:
            return False
    
