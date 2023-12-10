import datetime
from sqlalchemy.orm import aliased, Session
from sqlalchemy import update

import apps.timetable.models as user_models


def get_order_objects(db: Session, cort_id=None):
    current_time = datetime.datetime.now()
    last_ten_minutes = current_time - datetime.timedelta(minutes=10)
    starttime_table = aliased(user_models.TimeIntervalObjects)
    endtime_table = aliased(user_models.TimeIntervalObjects)
    result = db.query(user_models.Order, starttime_table, endtime_table).join(starttime_table, user_models.Order.starttime == starttime_table.id).join(endtime_table, user_models.Order.endtime == endtime_table.id).filter( (user_models.Order.payed==True) | (user_models.Order.time_created > last_ten_minutes) )
    if (cort_id):
        result = result.filter(user_models.Order.cort == cort_id)
    return result.all()

def get_repeatative_order_objects(db: Session, cort_id=None):
    starttime_table = aliased(user_models.TimeIntervalObjects)
    endtime_table = aliased(user_models.TimeIntervalObjects)
    result = db.query(user_models.TypicalRaspisanieObject, starttime_table, endtime_table).join(starttime_table, user_models.TypicalRaspisanieObject.starttime == starttime_table.id).join(endtime_table, user_models.TypicalRaspisanieObject.endtime == endtime_table.id)
    if (cort_id != None):
        result = result.filter(user_models.TypicalRaspisanieObject.cort == cort_id)
    return result.all()

def get_order_object(db: Session, id: int):
    current_time = datetime.datetime.now()
    last_ten_minutes = current_time - datetime.timedelta(minutes=10)
    starttime_table = aliased(user_models.TimeIntervalObjects)
    endtime_table = aliased(user_models.TimeIntervalObjects)
    return db.query(user_models.Order, starttime_table, endtime_table, user_models.Client).join(starttime_table, user_models.Order.starttime == starttime_table.id).join(endtime_table, user_models.Order.endtime == endtime_table.id).join(user_models.Client, user_models.Order.client == user_models.Client.id).filter(user_models.Order.id == id).filter( (user_models.Order.payed==True) | (user_models.Order.time_created > last_ten_minutes) ).first()

def set_order_paid(db: Session, id: int):
    db.execute(update(user_models.Order).where(user_models.Order.id==id).values(payed=True))
    db.commit()

def get_repeatative_order_object(db: Session, id: int):
    starttime_table = aliased(user_models.TimeIntervalObjects)
    endtime_table = aliased(user_models.TimeIntervalObjects)
    return db.query(user_models.TypicalRaspisanieObject, starttime_table, endtime_table).join(starttime_table, user_models.TypicalRaspisanieObject.starttime == starttime_table.id).join(endtime_table, user_models.TypicalRaspisanieObject.endtime == endtime_table.id).filter(user_models.TypicalRaspisanieObject.id == id).first()

def delete_order_object(db: Session, id: int) -> bool:
    timetable_object = db.query(user_models.Order).filter(user_models.Order.id == id).first()
    if (timetable_object):
        db.delete(timetable_object)
        db.commit()
        return True
    else:
        raise ValueError("Нет объекта с таким id")
        
def delete_repatative_order_object(db: Session, id: int) -> bool:
    timetable_object = db.query(user_models.TypicalRaspisanieObject).filter(user_models.TypicalRaspisanieObject.id == id).first()
    if (timetable_object):
        db.delete(timetable_object)
        db.commit()
        return True
    else:
        raise ValueError("Нет объекта с таким id")

def create_new_object(db: Session, date: datetime.date, starttime: datetime.time, endtime: datetime.time, payed: bool, client_name:str|None, client_phone: str|None, client_mail: str|None, bitrix_id: str|None, site_id: str|None, cort_id:int):
    time_start = db.query(user_models.TimeIntervalObjects).filter(user_models.TimeIntervalObjects.time_object == starttime).first()
    time_end = db.query(user_models.TimeIntervalObjects).filter(user_models.TimeIntervalObjects.time_object == endtime).first()
    if not(site_id):
        client = user_models.Client(client_bitrix_id=bitrix_id, client_name=client_name, client_phone=client_phone, client_mail=client_mail)
        db.add(client)
        db.commit()
        client_id = client.id
    else:
        client_id = site_id
    new_order = user_models.Order( date=date, starttime=time_start.id, endtime=time_end.id, payed=payed, client=int(client_id), cort=cort_id)
    db.add(new_order)
    db.commit()
    if (new_order.id):
        return new_order.id
    return False

def update_object_db(db: Session, date: datetime.date, starttime: datetime.time, endtime: datetime.time, payed: bool, client_name:str|None, client_phone: str|None, client_mail: str|None, bitrix_id: str|None, site_id: str|None, block_id:int, cort_id:int):
    order = db.query(user_models.Order).filter(user_models.Order.id == block_id).first()
    time_start = db.query(user_models.TimeIntervalObjects).filter(user_models.TimeIntervalObjects.time_object == starttime).first()
    time_end = db.query(user_models.TimeIntervalObjects).filter(user_models.TimeIntervalObjects.time_object == endtime).first()
    if not(site_id):
        client = user_models.Client(client_bitrix_id=bitrix_id, client_name=client_name, client_phone=client_phone, client_mail=client_mail)
        db.add(user_models.client)
        db.commit()
        client_id = user_models.client.id
    else:
        client_id = site_id
    db.execute(update(user_models.Order).where(user_models.Order.id==order.id).values(date=date, starttime=time_start.id, endtime=time_end.id, payed=payed, client=int(client_id), cort=cort_id))
    db.commit()

def create_new_repeatative_object(db: Session, starttime: datetime.time, endtime: datetime.time, description: str, weekdays: str, cort_id:int):
    time_start = db.query(user_models.TimeIntervalObjects).filter(user_models.TimeIntervalObjects.time_object == starttime).first()
    time_end = db.query(user_models.TimeIntervalObjects).filter(user_models.TimeIntervalObjects.time_object == endtime).first()
    db.add(user_models.TypicalRaspisanieObject( weekdays=weekdays, starttime=time_start.id, endtime=time_end.id, description=description, cort=cort_id))
    db.commit()
    return True

def update_repeatative_object_db(db: Session, block_id: int, starttime: datetime.time, endtime: datetime.time, description: str, weekdays: str, cort_id:int):
    order = db.query(user_models.TypicalRaspisanieObject).filter(user_models.TypicalRaspisanieObject.id == block_id).first()
    time_start = db.query(user_models.TimeIntervalObjects).filter(user_models.TimeIntervalObjects.time_object == starttime).first()
    time_end = db.query(user_models.TimeIntervalObjects).filter(user_models.TimeIntervalObjects.time_object == endtime).first()
    db.execute(update(user_models.TypicalRaspisanieObject).where(user_models.TypicalRaspisanieObject.id==order.id).values(weekdays=weekdays, starttime=time_start.id, endtime=time_end.id, description=description, cort=cort_id))
    db.commit()

def get_client_or_raise(db: Session, id: int) -> bool:
    timetable_object = db.query(user_models.Client).filter(user_models.Client.id == id).first()
    if (timetable_object):
        return True
    else:
        raise ValueError("Нет клиента с таким id")
        
def get_clients(db: Session) -> list:
    return db.query(user_models.Client).all()

def get_corts(db: Session) -> list:
    return db.query(user_models.Cort).all()

def get_intervals(db: Session) -> list:
    return db.query(user_models.TimeIntervalObjects).all()

def get_object_by_date(db: Session, date: datetime.date):
    return db.query(user_models.Order, user_models.TypicalRaspisanieObject).filter(user_models.Order.date==date).join(user_models.TypicalRaspisanieObject).all()


def get_links(db: Session, bitrix_id: int):

    current_time = datetime.datetime.now()
    starttime_table = aliased(user_models.TimeIntervalObjects)
    endtime_table = aliased(user_models.TimeIntervalObjects)

    cort_links = {
        1 : ["https://rtsp.me/embed/FSbsz932/", "https://rtsp.me/embed/FSbsz932/"],
        2 : ["https://rtsp.me/embed/FSbsz932/", "https://rtsp.me/embed/FSbsz932/"],
        3 : ["https://rtsp.me/embed/FSbsz932/", "https://rtsp.me/embed/FSbsz932/"],
        4 : ["https://rtsp.me/embed/FSbsz932/", "https://rtsp.me/embed/FSbsz932/"],
    }


    user_order = db.query(user_models.Order) \
        .join(user_models.Client, user_models.Client.id == user_models.Order.id) \
        .join(starttime_table, user_models.Order.starttime == starttime_table.id) \
        .join(endtime_table, user_models.Order.endtime == endtime_table.id) \
        .filter(user_models.Client.client_bitrix_id == bitrix_id, \
        user_models.Order.payed==True).first()
    
    if (user_order):
        return cort_links[user_order.cort] 
    else:
        raise ValueError("Расписание не найдено")