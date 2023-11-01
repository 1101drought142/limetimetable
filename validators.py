import datetime
from database import session, Order, TimeIntervalObjects
from sqlalchemy.orm import aliased

class OrderValidator():
    def __init__(self, 
        name : str,
        phone : str,
        starttime: datetime.time,
        endtime: datetime.time,
        date: datetime.date
    ):
        pass
        self.name = name
        self.phone = phone
        self.starttime = starttime
        self.endtime = endtime
        self.date = date

    def validate(self) -> bool:
        if (self.starttime >= self.endtime):
            raise ValueError("Invalid time given")
        if (self.starttime < datetime.time(8, 0, 0) or self.endtime > datetime.time(22, 0, 0)):
            raise ValueError("Invalid time given")
        starttime_table = aliased(TimeIntervalObjects)
        endtime_table = aliased(TimeIntervalObjects)
        objects = session.query(Order, starttime_table, endtime_table).join(starttime_table, Order.starttime == starttime_table.id).join(endtime_table, Order.endtime == endtime_table.id).all()

        for object, starttime, endtime in objects:

            if (object.date == self.date):
                if (self.starttime < starttime.time_object and self.starttime <= endtime.time_object):
                    pass
                elif (self.endtime >= starttime.time_object and self.endtime > endtime.time_object):
                    pass
        return True