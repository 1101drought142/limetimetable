import enum
import datetime
from sqlalchemy.orm import aliased, Session
from database import session, engine, Order, TimeIntervalObjects


def get_order_objects():
    starttime_table = aliased(TimeIntervalObjects)
    endtime_table = aliased(TimeIntervalObjects)
    return session.query(Order, starttime_table, endtime_table).join(starttime_table, Order.starttime == starttime_table.id).join(endtime_table, Order.endtime == endtime_table.id).all()

def create_new_object(date: datetime.date, starttime: datetime.time, endtime: datetime.time, payed: bool):
    with Session(autoflush=False, bind=engine) as db:
        time_start = db.query(TimeIntervalObjects).filter(TimeIntervalObjects.time_object == starttime).first()
        time_end = db.query(TimeIntervalObjects).filter(TimeIntervalObjects.time_object == endtime).first()
        db.add(Order( date=date, starttime=time_start.id, endtime=time_end.id, payed=False, client_bitrix_id=None, client_name="test", client_phone="test", client_mail="test"))
        db.commit()
        
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