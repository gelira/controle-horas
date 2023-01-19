from mongoengine import Document, fields, signals

from .utils import format_minutes, parse_time

class WorkingDate(Document):
    date = fields.StringField()
    total_worked_time = fields.StringField()
    total_worked_minutes = fields.IntField(default=0)

    @classmethod
    def get_or_create(cls, date):
        wd = cls.objects(date=date).first()

        if not wd:
            wd = cls(date=date)
            wd.save()

        return wd

    @classmethod
    def handle_pre_save(cls, sender, document, **kwargs):
        total_worked_minutes = document.total_worked_minutes

        if not total_worked_minutes:
            total_worked_minutes = 0

        document.total_worked_time = format_minutes(total_worked_minutes)

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
        start_time_dt = parse_time(document.start_time)
        end_time_dt = parse_time(document.end_time)

        if start_time_dt and end_time_dt:
            worked_minutes = (end_time_dt - start_time_dt).seconds // 60
        
        else:
            worked_minutes = 0
            document.end_time = ''

            if not start_time_dt:
                document.start_time = ''

        if worked_minutes < 0:
            worked_minutes += 60 * 60 * 24

        document.worked_minutes = worked_minutes
        document.worked_time = format_minutes(worked_minutes)

    @classmethod
    def handle_working_time_change(cls, sender, document, **kwargs):
        working_date = document.working_date

        if not working_date:
            return

        working_date.total_worked_minutes = cls.objects(working_date=working_date).sum('worked_minutes')
        working_date.save()

signals.pre_save.connect(WorkingDate.handle_pre_save, sender=WorkingDate)
signals.pre_save.connect(WorkingTime.handle_times_changes, sender=WorkingTime)
signals.post_save.connect(WorkingTime.handle_working_time_change, sender=WorkingTime)
signals.post_delete.connect(WorkingTime.handle_working_time_change, sender=WorkingTime)
