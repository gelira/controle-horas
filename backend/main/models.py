from mongoengine import Document, fields

class WorkingDate(Document):
    date = fields.StringField()
    total_worked_minutes = fields.IntField(default=0)

class WorkingTime(Document):
    working_date = fields.ReferenceField(WorkingDate)
    description = fields.StringField(default='')
    start_time = fields.StringField(default='')
    end_time = fields.StringField(default='')
    worked_minutes = fields.IntField(default=0)
    marked = fields.BooleanField(default=False)
