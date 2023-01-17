from mongoengine import Document, fields, signals
from datetime import datetime

class WorkingDate(Document):
    date = fields.StringField()
    total_worked_minutes = fields.IntField(default=0)

class WorkingTime(Document):
    working_date = fields.ReferenceField(WorkingDate)
    description = fields.StringField(default='')
    start_time = fields.StringField()
    end_time = fields.StringField()
    worked_time = fields.StringField()
    worked_minutes = fields.IntField(default=0)
    marked = fields.BooleanField(default=False)

    def calculate_worked_minutes(self):
        try:
            start_time_dt = datetime.strptime(self.start_time, '%H:%M')
        except:
            self.start_time = ''
            self.end_time = ''
            start_time_dt = None

        try:
            end_time_dt = datetime.strptime(self.end_time, '%H:%M')
        except:
            self.end_time = ''
            end_time_dt = None

        if start_time_dt and end_time_dt:
            worked_minutes = (end_time_dt - start_time_dt).seconds // 60
        else:
            worked_minutes = 0

        if worked_minutes < 0:
            worked_minutes += 60 * 60 * 24

        self.worked_minutes = worked_minutes

    def format_worked_time(self):
        hours = self.worked_minutes // 60
        minutes = self.worked_minutes % 60

        self.worked_time = f'{hours:02}:{minutes:02}'

def _pre_save_working_time(_, document, **kwargs):
    document.calculate_worked_minutes()
    document.format_worked_time()

signals.pre_save.connect(_pre_save_working_time, sender=WorkingTime)
