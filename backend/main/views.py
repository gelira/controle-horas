from ninja import NinjaAPI

from .models import WorkingDate, WorkingTime
from .dto import CreateWorkingTimeDTO, WorkingTimeOutDTO

api = NinjaAPI()

@api.post('/working-time', response=WorkingTimeOutDTO)
def create_working_time(request, payload: CreateWorkingTimeDTO):
    wd = WorkingDate.get_or_create(payload.date)

    wt = WorkingTime(working_date=wd)

    for key, value in payload.dict().items():
        if key != 'date':
            setattr(wt, key, value) 

    wt.save()

    return wt
