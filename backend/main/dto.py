from ninja import Schema
from pydantic import validator
from datetime import datetime

from .utils import parse_time

class CreateWorkingTimeDTO(Schema):
    date: str
    description: str = None
    start_time: str = None
    end_time: str = None

    @validator('date')
    def validate_date(cls, value):
        try:
            return datetime.strptime(value, '%Y-%m-%d') \
                .strftime('%Y-%m-%d')
        except:
            raise ValueError('date must be in YYYY-MM-DD format')

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
