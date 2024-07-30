from awsstations.models import TrainStation
from .models import AWSDataForquater

def updatetrain():
    for station in TrainStation.objects.all():
        stationdata = AWSDataForquater.objects.filter(station=station.neareststation).order_by('-timestamp')[:4]
        
        rainfall = max([d.rainfall for d in stationdata])
        if station.neareststation.station_id == 22:
            print(f'-------------------{rainfall}')
        if rainfall > 20:
            station.WarningLevel = 3
        elif rainfall > 15:
            station.WarningLevel = 2
        elif rainfall > 10:
            station.WarningLevel = 1
        else:
            station.WarningLevel = 0
        station.save()
