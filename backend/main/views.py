from ninja import NinjaAPI, Query
from ninja.errors import HttpError

from .models import WorkingDate, WorkingTime
from . import dto

api = NinjaAPI()

@api.get('/working-time', response=dto.WorkingDateOutDTO)
def list_working_time(request, query: dto.WorkingDateQuery = Query(...)):
    wd = WorkingDate.get_or_create(query.date)
    qs_with_st = WorkingTime.objects(working_date=wd, start_time__ne='').order_by('start_time')
    qs_without_st = WorkingTime.objects(working_date=wd, start_time='')

    return {
        'date': wd.date,
        'total_worked_time': wd.total_worked_time,
        'working_times': list(qs_with_st) + list(qs_without_st),
    }

@api.post('/working-time', response=dto.WorkingTimeOutDTO)
def create_working_time(request, payload: dto.CreateWorkingTimeDTO):
    wd = WorkingDate.get_or_create(payload.date)
    wt = WorkingTime(working_date=wd)

    for key, value in payload.dict().items():
        key != 'date' and setattr(wt, key, value)

    wt.save()

    return wt

@api.patch('/working-time', response=dto.WorkingTimeOutDTO)
def create_working_time(request, payload: dto.UpdateWorkingTimeDTO, query: dto.WorkingTimeQuery = Query(...)):
    wt = WorkingTime.objects(id=query.id).first()

    if not wt:
        raise HttpError(404, 'working time not found')

    for key, value in payload.dict().items():
        value is not None and setattr(wt, key, value)

    wt.save()

    return wt

@api.delete('/working-time', response={204: None})
def delete_working_time(request, query: dto.WorkingTimeQuery = Query(...)):
    wt = WorkingTime.objects(id=query.id).first()

    if not wt:
        raise HttpError(404, 'working time not found')

    wt.delete()

    return 204, None
