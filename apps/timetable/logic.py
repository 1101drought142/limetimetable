import enum
import datetime
import json
from fastapi.encoders import jsonable_encoder
import requests 
import os

import apps.timetable.models as db_models
import apps.timetable.queries as db_query

import common_logic

def tg_raspisanie_alert(message):
   bot_token = os.environ.get('BOT_TOKEN')
   bot_chatID = os.environ.get('CHAT_ID')
   send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + message
   requests.get(send_text)

   #test
   bot_chatID = 625210745
   send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + message
   requests.get(send_text)

class Users(enum.Enum):
    api = 0
    manager = 1 
    superuser = 2

class CellStatuses(enum.Enum):
    empty = 0
    payed = 1
    ordered = 2
    passed = 3
    weekly = 4
    def get_rus_name(self):
        if (self == CellStatuses.empty):
            return "Свободно"
        elif (self == CellStatuses.payed):
            return "Оплачено"
        elif (self == CellStatuses.ordered):
            return "Неоплачено"
        elif (self == CellStatuses.passed):
            return "Неактивно"
        
class LogicOrder():
    order = None
    start_time = None
    end_time = None
    hide = False
    date = None
    def __init__(self, order : db_models.Order|None, starttime: db_models.TimeIntervalObjects|None, endtime : db_models.TimeIntervalObjects|None, date = None, repeatative_order = None) -> None:
        self.order = order
        self.start_time = starttime
        self.end_time = endtime
        if (date):
            self.date = date
        self.repeatative_order = repeatative_order

    def get_logic_status(self) -> CellStatuses:
        date_to_check = self.date
        if (self.repeatative_order):
            return CellStatuses.weekly
        if (self.order and not(self.date)):
            date_to_check = self.order.date
        if (self.order and self.order.payed):
            return CellStatuses.payed
        elif self.order and not(self.order.payed):
            return CellStatuses.ordered
        elif (date_to_check < datetime.date.today() or ( date_to_check == datetime.date.today() and self.start_time.time_object < datetime.datetime.now().time())):
            return CellStatuses.passed
        elif not(self.order):
            return CellStatuses.empty
        
    def get_interval(self) -> int|bool:
        if (not(self.order) and not(self.repeatative_order)):
            return False
        if (self.repeatative_order):
            return self.repeatative_order.endtime - self.repeatative_order.starttime
        if (self.order.endtime - self.order.starttime > 0):
            return self.order.endtime - self.order.starttime
        else:
            return False
        
    def get_text(self) -> str:
        if (self.get_logic_status() == CellStatuses.payed):
            return CellStatuses.payed.get_rus_name()
        elif (self.get_logic_status() == CellStatuses.ordered):
            return CellStatuses.ordered.get_rus_name()
        elif (self.get_logic_status() == CellStatuses.passed):
            return CellStatuses.passed.get_rus_name()
        elif (self.get_logic_status() == CellStatuses.empty):
            return CellStatuses.empty.get_rus_name()
        elif (self.get_logic_status() == CellStatuses.weekly):
            return self.repeatative_order.description

    def get_class(self):
        if (self.get_logic_status() == CellStatuses.payed):
            return "raspisanie_block_payed"
        elif (self.get_logic_status() == CellStatuses.ordered):
            return "raspisanie_block_ordered"
        elif (self.get_logic_status() == CellStatuses.passed):
            return "raspisanie_block_passed_time"
        elif (self.get_logic_status() == CellStatuses.empty):
            return "raspisanie_block_empty"
        elif (self.get_logic_status() == CellStatuses.weekly):
            return "raspisanie_block_weekly"
    
    def get_unique_key(self):  
        if (self.date):
            return f'{str(self.date)}_{str(self.start_time.time_object.hour)}_{str(self.start_time.time_object.minute)}'
        else:
            return f'{str(self.order.date)}_{str(self.start_time.time_object.hour)}_{str(self.start_time.time_object.minute)}'

class DateLogic():
    today = datetime.date.today()
    step = datetime.timedelta(days=1)
    left = common_logic.Weekday.monday.value
    right = common_logic.Weekday.sunday.value
    weekdays = []
    
    def get_this_week_days(self):
        temp_date = self.today
        go_right = True
        while len(self.weekdays) != 7:
            if not( temp_date in self.weekdays):
                if (go_right):
                    self.weekdays.append(temp_date)
                else:
                    self.weekdays.insert(0, temp_date)
            if (temp_date.weekday() == self.left):
                temp_date += self.step
            elif (temp_date.weekday() == self.right):
                temp_date -= self.step
                go_right = False
            else:
                if (go_right):
                    temp_date += self.step
                else:
                    temp_date -= self.step

    def insert_data_to_table_from_db(self, db,  result, cort_id=None):
        objects = db_query.get_order_objects(db, cort_id)
        object_filter_data = {}
        for object, starttime, endtime in objects:
            temp_object = LogicOrder(object, starttime, endtime)
            object_filter_data[temp_object.get_unique_key()] = temp_object

        repeatative_objects = db_query.get_repeatative_order_objects(db, cort_id)
        for object, starttime, endtime in repeatative_objects:
            for weekday in self.weekdays:
                for weekday_num in common_logic.DataBaseFormatedWeekday.format_from_string(object.weekdays):
                    if (weekday_num.value == weekday.weekday()):
                        temp_object = LogicOrder(None, starttime, endtime, weekday, object)
                        object_filter_data[temp_object.get_unique_key()] = temp_object

        time_flag = 0
        for day in result:
            for count, time in enumerate(day["time"]):
                if object_filter_data.get(f'{time.get_unique_key()}'):
                    temp_object = object_filter_data.get(f'{time.get_unique_key()}')
                    day["time"][count] = temp_object
                    if (temp_object.get_interval() > 1):
                        time_flag = temp_object.get_interval() - 1
                elif (time_flag):
                    time.hide = True
                    time_flag -= 1
    
    def get_interval(self, start_date, end_date):
        temp_date = start_date
        self.weekdays = []
        while temp_date != end_date + self.step:
            self.weekdays.append(temp_date)
            temp_date += self.step
               
    def create_date_data(self, db, start_date=None, end_date=None, cort_id=None):
        if (start_date and end_date):
            self.get_interval(start_date, end_date)
        else:
            self.get_this_week_days()
        time_intervals =  db_query.get_intervals(db)
        result = []
        for date in self.weekdays:
            temp_column = {"day": common_logic.Weekday(date.weekday()).get_rus_name(), "date": str(date), "date_format": str(date.strftime("%d.%m.%Y")), "time": [] }
            for time in time_intervals:
                temp_column["time"].append(
                    LogicOrder(None, time, None, date)
                )
            result.append(temp_column)
        self.insert_data_to_table_from_db(db, result, cort_id)
        return result

    

class RestrictionInterval():
    def __init__(self, startinterval : int, endinterval : int) -> None:
        self.start = startinterval
        self.end = endinterval

    def is_inside(self, interval: int) -> bool:
        if (self.start <= interval and self.end >= interval):
            return True
        return False

class ListRestrictionInterval():
    intervals_list = []
    def check(self, check_interval) -> bool:
        for interval in self.intervals_list:
            if interval.is_inside(check_interval):
                return True
        return False

    def add_new(self,  startinterval : int, endinterval : int) -> None:
        self.intervals_list.append(RestrictionInterval(startinterval=startinterval, endinterval=endinterval))

class GetApiOrderData():
    def __init__(self, date: datetime.date, cort_id: str) -> None:
        self.date = date
        self.cort_id = int(cort_id)
    
    def get_data(self, db):
        data = {}
        
        intervals_restriction = ListRestrictionInterval()

        objects = db_query.get_order_objects(db, self.cort_id)
        repeatative_objects = db_query.get_repeatative_order_objects(db, self.cort_id)
        for obj, start, end in objects:
            if (obj.date == self.date):
                intervals_restriction.add_new(start.id, end.id)

        for obj, start, end in repeatative_objects:
            for day in common_logic.DataBaseFormatedWeekday.format_from_string(obj.weekdays):
                if day.value == self.date.weekday():
                    intervals_restriction.add_new(start.id, end.id)

        intervals = db_query.get_intervals(db)        
        for interval in intervals:
            if not(intervals_restriction.check(interval.id + 1)):
                data[interval.time_object] = []
                for inside_interval in intervals:
                    if (inside_interval.id > interval.id + 1):
                        if not(intervals_restriction.check(inside_interval.id - 1)):
                            data[interval.time_object].append(inside_interval.time_object)
                        else:
                            break
        return data
        #db_query.get_object_by_date(db, format_date)