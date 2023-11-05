import datetime
from sqlalchemy.orm import aliased

from database import DataBaseFormatedWeekday
from logic.utils import get_order_objects, create_new_object, get_client_or_raise, update_object_db, get_corts, create_new_repeatative_object

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
        cort_id: int,
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
        self.cort_id = int(cort_id)

    def validate(self) -> bool:

        if (self.starttime >= self.endtime):
            raise ValueError("Время окончания раньше времени начала")
        if (self.starttime < datetime.time(8, 0, 0) or self.endtime > datetime.time(23, 0, 0)):
            raise ValueError("Время не попадает в интервал работы корта")

        if (self.block_id):
            flag_object_exist = False
        else:
            flag_object_exist = True

        objects = get_order_objects(self.cort_id)
        for object, starttime, endtime in objects:
            if (object.id == self.block_id):
                flag_object_exist = True
                continue
            if (object.date == self.date):
                if not((self.starttime < starttime.time_object and self.endtime <= starttime.time_object) or (self.starttime >= endtime.time_object and self.endtime > endtime.time_object)):
                    raise ValueError("Время совпадает с занятым временем")
        
        if (not(flag_object_exist)):
            raise ValueError("Заказа с таким ID нет")
        
        cort_flag = False
        corts = get_corts()
        for cort in corts:
            if (cort.id == self.cort_id):
                cort_flag = True

        if not(cort_flag):
            raise ValueError("Корта с таким id не существует")
        
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
            self.site_id,
            self.cort_id
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
            self.block_id,
            self.cort_id
            )):
            return True
        else:
            return False
        


class RepeatativeTaskValidator():
    def __init__(self,
        start_time,
        end_time,
        description,
        days,
        cort_id
    ) -> None:
        self.start_time = start_time
        self.end_time = end_time
        self.description = description
        self.days = days
        self.cort_id = int(cort_id)

    def validate(self) -> bool:
        self.start_time_format = datetime.datetime.strptime(self.start_time, '%H:%M').time()
        self.end_time_format = datetime.datetime.strptime(self.end_time, '%H:%M').time()
        if ( self.start_time_format >  self.end_time_format):
            raise ValueError("Время начала позже время начала")
        
        DataBaseFormatedWeekday.check_if_valid_or_raise(self.days)
        
        cort_flag = False
        corts = get_corts()
        for cort in corts:
            if (cort.id == self.cort_id):
                cort_flag = True

        if not(cort_flag):
            raise ValueError("Корта с таким id не существует")
        
        objects = get_order_objects(self.cort_id)
        #for object, starttime, endtime in objects:
            #Переписать проверку
            # if (object.date == self.date):
            #     if not((self.starttime < starttime.time_object and self.endtime <= starttime.time_object) or (self.starttime >= endtime.time_object and self.endtime > endtime.time_object)):
            #         raise ValueError("Время совпадает с занятым временем")

        #print(DataBaseFormatedWeekday.from_list_to_string(self.days))
        return True

    def create_object(self):
        if (create_new_repeatative_object(self.start_time_format, self.end_time_format, self.description, DataBaseFormatedWeekday.from_list_to_string(self.days), self.cort_id)):
            return True
        else:
            return False