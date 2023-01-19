from ninja import Schema
from pydantic import validator

from .utils import parse_time, validate_date

class WorkingDateQuery(Schema):
    date: str
    _validate_date = validator('date', allow_reuse=True)(validate_date)

class CreateWorkingTimeDTO(Schema):
    date: str
    description: str = None
    start_time: str = None
    end_time: str = None
    _validate_date = validator('date', allow_reuse=True)(validate_date)

    @validator('start_time', 'end_time')
    def validate_times(cls, value):
        dt = parse_time(value)
        return dt and dt.strftime('%H:%M')

class WorkingTimeOutDTO(Schema):
    _id: str
    description: str
    start_time: str
    end_time: str
    worked_time: str
    marked: bool
