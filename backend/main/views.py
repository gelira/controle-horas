from ninja import NinjaAPI, Query
from ninja.errors import HttpError

from .models import WorkingDate, WorkingTime
from .dto import (
    WorkingTimeQuery,
    WorkingDateQuery,
    CreateWorkingTimeDTO, 
    WorkingTimeOutDTO,
    WorkingDateOutDTO
)

api = NinjaAPI()

@api.get('/working-time', response=WorkingDateOutDTO)
def list_working_time(request, query: WorkingDateQuery = Query(...)):
    wd = WorkingDate.get_or_create(query.date)
    qs = WorkingTime.objects(working_date=wd).order_by('start_time')

    return {
        'date': wd.date,
        'total_worked_time': wd.total_worked_time,
        'working_times': list(qs),
    }

@api.post('/working-time', response=WorkingTimeOutDTO)
def create_working_time(request, payload: CreateWorkingTimeDTO):
    wd = WorkingDate.get_or_create(payload.date)
    wt = WorkingTime(working_date=wd)

    for key, value in payload.dict().items():
        if key != 'date':
            setattr(wt, key, value) 

    wt.save()

    return wt

@api.delete('/working-time', response={204: None})
def delete_working_time(request, query: WorkingTimeQuery = Query(...)):
    wt = WorkingTime.objects(id=query.id).first()

    if not wt:
        raise HttpError(404, 'working time not found')

    wt.delete()

    return 204, None
