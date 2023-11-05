import datetime
import enum
from sqlalchemy.orm import joinedload, aliased

from database import session, Order, TimeIntervalObjects, Weekday, DataBaseFormatedWeekday
from logic.utils import get_order_objects, get_repeatative_order_objects

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
    def __init__(self, order : Order|None, starttime: TimeIntervalObjects|None, endtime : TimeIntervalObjects|None, date = None, repeatative_order = None) -> None:
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
    left = Weekday.monday.value
    right = Weekday.sunday.value
    weekdays = []
    
    def get_date_interval(self):
        result = session.query(TimeIntervalObjects).all()
        return result
    
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

    def insert_data_to_table_from_db(self, result, cort_id=None):
        objects = get_order_objects(cort_id)
        object_filter_data = {}
        for object, starttime, endtime in objects:
            temp_object = LogicOrder(object, starttime, endtime)
            object_filter_data[temp_object.get_unique_key()] = temp_object

        repeatative_objects = get_repeatative_order_objects(cort_id)
        for object, starttime, endtime in repeatative_objects:
            for weekday in self.weekdays:
                for weekday_num in DataBaseFormatedWeekday.format_from_string(object.weekdays):
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
               

    def create_date_data(self, start_date=None, end_date=None, cort_id=None):
        if (start_date and end_date):
            self.get_interval(start_date, end_date)
        else:
            self.get_this_week_days()
        time_intervals = self.get_date_interval() 
        result = []
        for date in self.weekdays:
            temp_column = {"day": Weekday(date.weekday()).get_rus_name(), "date": str(date), "time": [] }
            for time in time_intervals:
                temp_column["time"].append(
                    LogicOrder(None, time, None, date)
                )
            result.append(temp_column)
        self.insert_data_to_table_from_db(result, cort_id)
        return result