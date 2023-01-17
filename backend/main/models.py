from mongoengine import Document, fields, signals
from datetime import datetime

class WorkingDate(Document):
    date = fields.StringField()
    total_worked_time = fields.StringField()
    total_worked_minutes = fields.IntField(default=0)

class WorkingTime(Document):
    working_date = fields.ReferenceField(WorkingDate)
    description = fields.StringField(default='')
    start_time = fields.StringField()
    end_time = fields.StringField()
    worked_time = fields.StringField()
    worked_minutes = fields.IntField(default=0)
    marked = fields.BooleanField(default=False)

    @classmethod
    def handle_times_changes(cls, sender, document, **kwargs):
        try:
            start_time_dt = datetime.strptime(document.start_time, '%H:%M')
        except:
            document.start_time = ''
            document.end_time = ''
            start_time_dt = None

        try:
            end_time_dt = datetime.strptime(document.end_time, '%H:%M')
        except:
            document.end_time = ''
            end_time_dt = None

        if start_time_dt and end_time_dt:
            worked_minutes = (end_time_dt - start_time_dt).seconds // 60
        else:
            worked_minutes = 0

        if worked_minutes < 0:
            worked_minutes += 60 * 60 * 24

        document.worked_minutes = worked_minutes

        hours = worked_minutes // 60
        minutes = worked_minutes % 60

        document.worked_time = f'{hours:02}:{minutes:02}'

    @classmethod
    def handle_working_time_change(cls, sender, document, **kwargs):
        working_date = document.working_date

        if not working_date:
            return

        total_worked_minutes = cls.objects(working_date=working_date).sum('worked_minutes')

        hours = total_worked_minutes // 60
        minutes = total_worked_minutes % 60

        working_date.total_worked_time = f'{hours:02}:{minutes:02}'
        working_date.total_worked_minutes = total_worked_minutes
        working_date.save()

signals.pre_save.connect(WorkingTime.handle_times_changes, sender=WorkingTime)
signals.post_save.connect(WorkingTime.handle_working_time_change, sender=WorkingTime)
