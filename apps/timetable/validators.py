import datetime

import apps.timetable.queries as db_query
import apps.timetable.schemas as schemas

from common_logic import DataBaseFormatedWeekday


class BaseTimeBlockValidator():

    def timevalidation(self, starttime: datetime.time, endtime: datetime.time):
        if (starttime >= endtime):
            raise ValueError("Время окончания раньше времени начала")
        if (starttime < datetime.time(8, 0, 0) or endtime > datetime.time(23, 0, 0)):
            raise ValueError("Время не попадает в интервал работы корта")

    def cortvalidation(self, cort_id: int):
        cort_flag = False
        corts = db_query.get_corts(self.db)
        for cort in corts:
            if (cort.id == cort_id):
                cort_flag = True

        if not(cort_flag):
            raise ValueError("Корта с таким id не существует")
    
class OrderValidator(BaseTimeBlockValidator):
    def __init__(self, 
        db,
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
        self.db = db
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

    def validate_and_get_object_or_raise(self) -> schemas.ValidatedOrderObject:

        self.timevalidation(self.starttime, self.endtime)
        self.cortvalidation(self.cort_id)

        if (self.block_id):
            flag_object_exist = False
        else:
            flag_object_exist = True
                
        if (not(flag_object_exist)):
            raise ValueError("Заказа с таким ID нет")
        
        objects = db_query.get_order_objects(self.db, self.cort_id)
        for object, starttime, endtime in objects:
            if (object.id == self.block_id):
                flag_object_exist = True
                continue
            if (object.date == self.date):
                if not((self.starttime < starttime.time_object and self.endtime <= starttime.time_object) or (self.starttime >= endtime.time_object and self.endtime > endtime.time_object)):
                    raise ValueError("Время совпадает с занятым временем")
                
        repeatative_objects = db_query.get_repeatative_order_objects(self.db, self.cort_id)
        for object, starttime, endtime in repeatative_objects:
            for db_date in DataBaseFormatedWeekday.format_from_string(object.weekdays):
                if self.date.weekday() == db_date.value:
                    if not((self.starttime < starttime.time_object and self.endtime <= starttime.time_object) or (self.starttime >= endtime.time_object and self.endtime > endtime.time_object)):
                        raise ValueError("Время совпадает с занятым временем")

        if (not(self.site_id) and not(self.name and self.phone and self.mail)):
            raise ValueError("Нет данных о клиенте")

        if (self.site_id):
            db_query.get_client_or_raise(self.db, self.site_id)

        return schemas.ValidatedOrderObject(
            date = self.date,
            starttime = self.starttime,
            endtime = self.endtime,
            payed = self.payed,
            name = self.name,
            phone = self.phone,
            mail = self.mail,
            bitrix_id = self.bitrix_id,
            site_id = self.site_id,
            cort_id = self.cort_id,
            block_id = self.block_id    
        )
        


class RepeatativeTaskValidator(BaseTimeBlockValidator):
    def __init__(self,
        db,
        start_time : datetime.time,
        end_time: datetime.time,
        description : str,
        days : list,
        cort_id : int,
        block_id = None
    ) -> None:
        self.db = db
        self.start_time = start_time
        self.end_time = end_time
        self.description = description
        self.days = days
        self.cort_id = int(cort_id)
        self.block_id = block_id

    def validate_and_get_object_or_raise(self) -> bool:

        self.timevalidation(self.starttime, self.endtime)
        self.cortvalidation(self.cort_id)

        DataBaseFormatedWeekday.check_if_valid_or_raise(self.days)
        
        
        if not(self.days):
            raise ValueError("Дни недели не выбраны")
        
        objects = db_query.get_order_objects(self.db, self.cort_id)
        for object, starttime, endtime in objects:
            for db_date in self.days:
                if int(object.date.weekday()) == int(db_date):
                    if not((self.start_time < starttime.time_object and self.end_time <= starttime.time_object) or (self.start_time >= endtime.time_object and self.end_time > endtime.time_object)):
                        raise ValueError("Время совпадает с занятым временем")
                
        repeatative_objects = db_query.get_repeatative_order_objects(self.db, self.cort_id)
        for object, starttime, endtime in repeatative_objects:
            for db_date in DataBaseFormatedWeekday.format_from_string(object.weekdays):
                for new_date in self.days:
                    if int(new_date) == db_date.value:
                        if not((self.start_time < starttime.time_object and self.end_time <= starttime.time_object) or (self.start_time >= endtime.time_object and self.end_time > endtime.time_object)):
                            raise ValueError("Время совпадает с занятым временем")
        
        return schemas.ValidatedRepeatativeOrderObject(
            starttime = self.start_time,
            endtime = self.end_time,
            description = self.description,
            weekdays = DataBaseFormatedWeekday.from_list_to_string(self.days),
            cort_id = self.cort_id,
            block_id = self.block_id
        )