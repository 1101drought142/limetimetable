import datetime
import enum

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

class DataBaseFormatedWeekday():
    def format_to_string(weekdays):
        res_string = ""
        for weekday in weekdays:
            res_string += f'{weekday.value},'
        return res_string
    
    def format_from_string(string):
        res = []
        raw_array = string.split(",")
        for el in raw_array:
            if (el):
                res.append(Weekday(int(el)))
        return res

    def from_list_to_string(weekdays):
        res_string = ""
        for weekday in weekdays:
            res_string += f'{weekday},'
        return res_string

    def check_if_valid_or_raise(weekdays):
        for weekday in weekdays:
            try:
                Weekday(int(weekday))
            except:
                raise ValueError("Неправильный день недели")


def datetime_picker_format(date : datetime.datetime):
    return date.strftime("%d-%m-%Y %H:%M")

def time_picker_format(date : datetime.time):
    return date.strftime("%H:%M")