import datetime
import enum

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
        result = [
            "10",
            "11",
            "12",
            "13",
            "14",
            "15",
            "16",
            "17",
            "18",
            "19",
            "20",
        ]
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
                    }
                )
            result.append(temp_column)
        return result
test = DateLogic()
print(test.create_date_data())