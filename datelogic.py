import datetime
import enum
from sqlalchemy.orm import joinedload, aliased

from database import session, Order, TimeIntervalObjects

class CellStatuses(enum.Enum):
    empty = "empty"
    payed = "payed"
    passed = "passed"
    def get_rus_name(self):
        if (self == CellStatuses.empty):
            return "Свободно"
        elif (self == CellStatuses.payed):
            return "Оплачено"
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
            temp_object= {}
            temp_object["text"] = "test"
            temp_object["starttime"] = starttime.time_object
            temp_object["endtime"] = endtime.time_object
            temp_object["timeinterval"] = int(endtime.id - starttime.id)
            temp_object["payed"] = object.payed

            if (object.payed):
                temp_object["class"] = "raspisanie_block_payed"
            else:
                temp_object["class"] = "raspisanie_block_ordered"
            object_filter_data[f'{str(object.date)}_{str(starttime.time_object.hour)}_{str(starttime.time_object.minute)}'] = temp_object
        print(object_filter_data)
        time_flag = 0
        for day in result:
            for time in day["time"]:
                if object_filter_data.get(f'{str(day["date"])}_{str(time["time"].hour)}_{str(time["time"].minute)}'):
                    temp_object = object_filter_data.get(f'{str(day["date"])}_{str(time["time"].hour)}_{str(time["time"].minute)}')
                    print(f'{str(day["date"])}_{str(time["time"].hour)}_{str(starttime.time_object.minute)}')
                    print(temp_object)
                    time["text"] = "Занято расписание"
                    time["class"] = temp_object["class"]
                    if (temp_object["timeinterval"] > 1):
                        time_flag = temp_object["timeinterval"] - 1
                        time["rowspan"] = temp_object["timeinterval"]
                elif (time_flag):
                    time["hide"] = True
                    time_flag -= 1
                    
    def create_date_data(self):
        self.get_this_week_days()
        time_intervals = self.get_date_interval() 
        result = []
        for date in self.weekdays:
            temp_column = {"day": Weekday(date.weekday()).get_rus_name(), "date": str(date), "time": [] }
            for time in time_intervals:
                temp_column["time"].append(
                    {
                        "status" : CellStatuses.empty.value,
                        "text" : CellStatuses.empty.get_rus_name(),
                        "time": datetime.time(hour=time.time_object.hour, minute=time.time_object.minute),
                        "class": "raspisanie_block_empty"
                    }
                )
            result.append(temp_column)
        self.insert_data_to_table_from_db(result)
        return result