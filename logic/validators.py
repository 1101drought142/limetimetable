import datetime
from sqlalchemy.orm import aliased

from database import session, Order, TimeIntervalObjects
from logic.utils import get_order_objects, create_new_object, get_client_or_raise, update_object_db

class OrderValidator():
    def __init__(self, 
        name : str|None,
        phone : str|None,
        mail: str|None,
        payed: bool,
        starttime: datetime.time,
        endtime: datetime.time,
        date: datetime.date,
        bitrix_id: int|None,
        site_id: int|None, 
        block_id: str|None,

    ):
        self.name = name
        self.phone = phone
        self.mail = mail
        self.payed = payed
        self.starttime = starttime
        self.endtime = endtime
        self.date = date
        self.bitrix_id = bitrix_id
        self.site_id = site_id
        self.block_id = block_id

    def validate(self) -> bool:

        if (self.starttime >= self.endtime):
            raise ValueError("Время окончания раньше времени начала")
        if (self.starttime < datetime.time(8, 0, 0) or self.endtime > datetime.time(23, 0, 0)):
            raise ValueError("Время не попадает в интервал работы корта")

        if (self.block_id):
            flag_object_exist = False
        else:
            flag_object_exist = True

        objects = get_order_objects()
        for object, starttime, endtime in objects:
            if (object.id == self.block_id):
                flag_object_exist = True
                continue
            if (object.date == self.date):
                if not((self.starttime < starttime.time_object and self.endtime <= starttime.time_object) or (self.starttime >= endtime.time_object and self.endtime > endtime.time_object)):
                    raise ValueError("Время совпадает с занятым временем")
                
        if (not(flag_object_exist)):
            raise ValueError("Заказа с таким ID нет")
        
        if (not(self.site_id) and not(self.name and self.phone and self.mail)):
            raise ValueError("Нет данных о клиенте")

        if (self.site_id):
            get_client_or_raise(self.site_id)

        return True
    
    def create_object(self):
        if (create_new_object(
            self.date, 
            self.starttime, 
            self.endtime, 
            self.payed, 
            self.name,
            self.phone,
            self.mail,
            self.bitrix_id,
            self.site_id
            )):
            return True
        else:
            return False
    
    def update_object(self):
        if (update_object_db(
            self.date, 
            self.starttime, 
            self.endtime, 
            self.payed, 
            self.name,
            self.phone,
            self.mail,
            self.bitrix_id,
            self.site_id,
            self.block_id
            )):
            return True
        else:
            return False