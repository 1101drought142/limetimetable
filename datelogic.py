import datetime
import enum
from sqlalchemy.orm import joinedload, aliased

from database import session, Order, TimeIntervalObjects

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
            return "Время прошло"
        
class Weekday(enum.Enum):
    monday = 0
    tuesday = 1
    wednesday = 2
    thursday = 3
    friday = 4
    saturday = 5
    sunday = 6
    def get_rus_name(self):
        if (self == Weekday.monday):
            return "Понедельник"
        elif (self == Weekday.tuesday):
            return "Вторник"
        elif (self == Weekday.wednesday):
            return "Среда"
        elif (self == Weekday.thursday):
            return "Четверг"
        elif (self == Weekday.friday):
            return "Пятница"
        elif (self == Weekday.saturday):
            return "Суббота"
        elif (self == Weekday.sunday):
            return "Воскресенье"

class LogicOrder():
    order = None
    start_time = None
    end_time = None
    hide = False
    date = None
    def __init__(self, order : Order|None, starttime: TimeIntervalObjects|None, endtime : TimeIntervalObjects|None, date = None) -> None:
        self.order = order
        self.start_time = starttime
        self.end_time = endtime
        if (date):
            self.date = date
    def get_logic_status(self) -> CellStatuses:
        date_to_check = self.date
        if (self.order and not(self.date)):
            date_to_check = self.order.date
        if (date_to_check < datetime.date.today() or ( date_to_check == datetime.date.today() and self.start_time.time_object < datetime.datetime.now().time())):
            return CellStatuses.passed
        elif not(self.order):
            return CellStatuses.empty
        elif (self.order.payed):
            return CellStatuses.payed
        elif not(self.order.payed):
            return CellStatuses.ordered
        
    
    def get_interval(self) -> int|bool:
        if (not(self.order)):
            return False
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

    def get_class(self):
        if (self.get_logic_status() == CellStatuses.payed):
            return "raspisanie_block_payed"
        elif (self.get_logic_status() == CellStatuses.ordered):
            return "raspisanie_block_ordered"
        elif (self.get_logic_status() == CellStatuses.passed):
            return "raspisanie_block_passed_time"
        elif (self.get_logic_status() == CellStatuses.empty):
            return "raspisanie_block_empty"
    
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

    def insert_data_to_table_from_db(self, result):
        starttime_table = aliased(TimeIntervalObjects)
        endtime_table = aliased(TimeIntervalObjects)
        objects = session.query(Order, starttime_table, endtime_table).join(starttime_table, Order.starttime == starttime_table.id).join(endtime_table, Order.endtime == endtime_table.id).all()
        object_filter_data = {}
        for object, starttime, endtime in objects:
            temp_object = LogicOrder(object, starttime, endtime)
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
                    
    def create_date_data(self):
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
        self.insert_data_to_table_from_db(result)
        return result