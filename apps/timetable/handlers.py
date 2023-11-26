from pydantic import BaseModel
import datetime

import apps.timetable.schemas as schemas 
import apps.timetable.queries as db_query
import apps.timetable.validators as db_validators
from apps.timetable.logic import DateLogic, GetApiOrderData

from database import get_db

from common_logic import datetime_picker_format, Weekday, DataBaseFormatedWeekday, time_picker_format

class GetAddOrderTemplateHandler(BaseModel):
    start_time : str
    date: str

    def get_validated_result(self, db):
        start_time = datetime.datetime.fromisoformat(f"{self.date} {self.start_time}") 
        end_time = start_time + datetime.timedelta(hours=1)
        return schemas.AddOrderScheme(
            start_time = datetime_picker_format(start_time),
            end_time = datetime_picker_format(end_time),
            clients = db_query.get_clients(db),
            corts = db_query.get_corts(db),
        )
    
class GetChangeModalTemplateHandler(BaseModel):
    block_id : str

    def get_validated_result(self, db):
        order_object = db_query.get_order_object(db, int(self.block_id))
        order, start_time_db, end_time_db, client = order_object
        date = order.date
        start_timeinterval = start_time_db.time_object
        end_timeinterval = end_time_db.time_object
        start_time = datetime.datetime(year=date.year, month=date.month, day=date.day, hour=start_timeinterval.hour, minute=start_timeinterval.minute)
        end_time = datetime.datetime(year=date.year, month=date.month, day=date.day, hour=end_timeinterval.hour, minute=end_timeinterval.minute)
        return schemas.GetChangeModalScheme (
            start_time = datetime_picker_format(start_time),
            end_time = datetime_picker_format(end_time),
            order = order,
            client = client,
            clients = db_query.get_clients(db),
            corts = db_query.get_corts(db),
        )

class GetAddRepeatativeBlockModalTemplate(BaseModel): 
    def get_validated_result(self, db):
        return schemas.AddRepeatativeBlockScheme (
            corts = db_query.get_corts(db),
            weekdays = [e for e in Weekday],
        )

class GetChangeModalRepeatativeTemplateHandler(BaseModel):
    block_id : str

    def get_validated_result(self, db):
        repeatative_order_object = db_query.get_repeatative_order_object(db, int(self.block_id))
        repeatative_order, start_time_db, end_time_db = repeatative_order_object
        start_timeinterval = start_time_db.time_object
        end_timeinterval = end_time_db.time_object
        start_time = datetime.datetime(year=2021, month=1, day=1, hour=start_timeinterval.hour, minute=start_timeinterval.minute)
        end_time = datetime.datetime(year=2021, month=1, day=1, hour=end_timeinterval.hour, minute=end_timeinterval.minute)
        return schemas.GetChangeModalRepeatativeScheme (
            start_time = time_picker_format(start_time),
            end_time = time_picker_format(end_time),
            repeatative_order = repeatative_order,
            corts = db_query.get_corts(db),
            weekdays = [e for e in Weekday],
            curent_weekdays =  DataBaseFormatedWeekday.format_from_string(repeatative_order.weekdays),
        )

class CreateNewTimeBlock(BaseModel):
    date_start: str
    date_end: str
    status: bool
    client_name: str
    client_phone: str
    client_mail: str
    client_bitrix_id: str
    client_site_id: str
    cort_id: str

    def execute_query(self, db):
        start_time = datetime.datetime.strptime(self.date_start, '%d-%m-%Y %H:%M')
        end_time = datetime.datetime.strptime(self.date_end, '%d-%m-%Y %H:%M')
        try:
            validator = db_validators.OrderValidator(db, self.client_name, self.client_phone, self.client_mail, self.status, start_time.time(), end_time.time(), start_time.date(), self.client_bitrix_id, self.client_site_id, None, self.cort_id)
            validator_result = validator.validate_and_get_object_or_raise()
            db_query.create_new_object(
                db, 
                validator_result.date, 
                validator_result.starttime, 
                validator_result.endtime, 
                validator_result.payed, 
                validator_result.name,
                validator_result.phone,
                validator_result.mail,
                validator_result.bitrix_id,
                validator_result.site_id,
                validator_result.cort_id
            )
        except Exception as ex:
            return ex
        return True

class ChangeTimeBlock(BaseModel):
    block_id: str
    date_start: str
    date_end: str
    status: bool
    client_name: str
    client_phone: str
    client_mail: str
    client_bitrix_id: str
    client_site_id: str
    cort_id: str

    def execute_query(self, db):
        start_time = datetime.datetime.strptime(self.date_start, '%d-%m-%Y %H:%M')
        end_time = datetime.datetime.strptime(self.date_end, '%d-%m-%Y %H:%M')
        try:
            validator = db_validators.OrderValidator(db, self.client_name, self.client_phone, self.client_mail, self.status, start_time.time(), end_time.time(), start_time.date(), self.client_bitrix_id, self.client_site_id, int(self.block_id), self.cort_id)
            validator_result = validator.validate_and_get_object_or_raise()
            db_query.update_object_db(
                db, 
                validator_result.date, 
                validator_result.starttime, 
                validator_result.endtime, 
                validator_result.payed, 
                validator_result.name,
                validator_result.phone,
                validator_result.mail,
                validator_result.bitrix_id,
                validator_result.site_id,
                validator_result.block_id,
                validator_result.cort_id
            )
        except Exception as ex:
            return ex
        return True

class CreateRepeatativeTimeBlock(BaseModel):
    time_start: str
    time_end: str
    description: str
    days: list
    cort_id: str

    def execute_query(self, db):
        start_time = datetime.datetime.strptime(self.time_start, '%H:%M')
        end_time = datetime.datetime.strptime(self.time_end, '%H:%M')
        try:
            validator = db_validators.RepeatativeTaskValidator(db, start_time.time(), end_time.time(), self.description, self.days, self.cort_id)
            validator_result = validator.validate_and_get_object_or_raise()
            db_query.create_new_repeatative_object(
                db, 
                validator_result.starttime, 
                validator_result.endtime, 
                validator_result.description, 
                validator_result.weekdays, 
                validator_result.cort_id
            )
        except Exception as ex:
            return ex
        return True

class ChangeRepeatativeTimeBlock(BaseModel):
    block_id: str
    time_start: str
    time_end: str
    description: str
    days: list
    cort_id: str

    def execute_query(self, db):
        start_time = datetime.datetime.strptime(self.time_start, '%H:%M')
        end_time = datetime.datetime.strptime(self.time_end, '%H:%M')
        try:
            validator = db_validators.RepeatativeTaskValidator(db, start_time.time(), end_time.time(), self.description, self.days, self.cort_id, self.block_id)
            validator_result = validator.validate_and_get_object_or_raise()
            db_query.update_repeatative_object_db(
                db, 
                validator_result.block_id, 
                validator_result.starttime, 
                validator_result.endtime, 
                validator_result.description, 
                validator_result.weekdays, 
                validator_result.cort_id
            )
        except Exception as ex:
            return ex
        return True

class DeleteTimeBlock(BaseModel):
    block_id: str

    def execute_query(self, db):
        try:
            db_query.delete_order_object(db, int(self.block_id))
        except Exception as ex:
            return ex
        return True

class DeleteRepeatativeTimeBlock(BaseModel):
    block_id: str

    def execute_query(self, db):
        try:
            db_query.delete_repatative_order_object(db, int(self.block_id))
        except Exception as ex:
            return ex
        return True

class GetFilteredTable(BaseModel):
    date_range: str
    cort_id: str

    def get_validated_result(self, db):
        if (self.date_range):
            start_date_str, end_date_str = self.date_range.replace(" ", "").split("-")
            start_date = datetime.datetime.strptime(start_date_str,'%d.%m.%Y').date()
            end_date = datetime.datetime.strptime(end_date_str, '%d.%m.%Y').date()
        else:
            start_date = end_date = None
        cort_id = 1
        if (self.cort_id):
            cort_id = self.cort_id
        data = DateLogic().create_date_data(db, start_date, end_date, cort_id)

        return schemas.TableScheme(
            data = data,
            timerange = db_query.get_intervals(db),
        )
    
class GetRaspisanie(BaseModel):
    date: str

    def execute_query(self, db):
        day, month, year =  self.date.split(".")
        try:
            format_date = datetime.date(day=int(day), month=int(month), year=int(year))
            validator = GetApiOrderData(format_date)
            return validator.get_data(db)
        except Exception as ex:
            return ex