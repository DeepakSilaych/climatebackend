from django.shortcuts import render
from awsstations.models import *
from awsstations.serializers import *
from crowdsource.models import *
from crowdsource.serializers import *
from .models import *


from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.db import connection
from django.db.utils import OperationalError
from django.utils import timezone
from datetime import timedelta

from django.db.models import Sum
from django.db.models.functions import TruncHour
from django.utils.timezone import now
from django.utils.timezone import make_aware
from datetime import datetime


class AWSStationListView(APIView):
    def get(self, request):
        stations = AWSStation.objects.all().order_by('name')
        serializer = AWSStationSerializer(stations, many=True)
        return Response(serializer.data)
    
class StationDataListView(APIView):
    def post(self, request):
        print(request.data)
        StationData.objects.create(
            station=AWSStation.objects.get(station_id=request.data['station']), 
            rainfall=request.data['rainfall']
        )
        return Response({'status': 'success'})
    
    def get(self, request):
        station = AWSStation.objects.get(station_id=request.query_params.get('station', None))
        if station is not None:
            stationdata = StationData.objects.filter(station=station).order_by('-timestamp')[:100]
        else:
            stationdata = StationData.objects.all().order_by('-timestamp')[:100]
        serializer = StationDataSerializer(stationdata, many=True)
        return Response(serializer.data)

class AWSDataForquaterListView(APIView):
    def post(self, request):
        station = AWSStation.objects.get(station_id=request.data['station'])
        AWSDataForquater.objects.create(
            station=station,
            rainfall=request.data['rainfall']
        )
        
        try:
            trainstations = TrainStation.objects.filter(neareststation=station)
            for trainstation in trainstations:
                updatetrain(trainstation)
        except:
            pass

        return Response({'status': 'success'})

class DaywisePredictionListView(APIView):
    def post(self, request):
        station = AWSStation.objects.get(station_id=request.data['station'])
        station.rainfall = request.data['day1']
        station.save()

        try :
            DaywisePrediction.objects.create(
                station=station,
                timestamp= datetime.strptime(request.data['date'], '%Y-%m-%d %H:%M:%S'),
                day1_rainfall=request.data['day1'],
                day2_rainfall=request.data['day2'],
                day3_rainfall=request.data['day3']
            )

        except :
            DaywisePrediction.objects.create(
                station=station,
                day1_rainfall=request.data['day1'],
                day2_rainfall=request.data['day2'],
                day3_rainfall=request.data['day3']
            )
        return Response({'status': 'success'})

class HourlyPredictionListView(APIView):
    def post(self, request):
        print(request.data)
        HourlyPrediction.objects.create(
            station=AWSStation.objects.get(station_id=request.data['station']),
            hr_24_rainfall=request.data.getlist('hr_24_rainfall')
        )
        return Response({'status': 'success'})
    
class SaveTweet(APIView):
    def post(self, request):
        Tweets.objects.create(
            tweet_text=request.data['tweet'],
            timestamp=request.data['timestamp'],
            sentiment=request.data['sentiment'] == 'POSITIVE',
            latitude=request.data['latitude'],
            longitude=request.data['longitude'],
            address=request.data['location']
        )
        return Response({'status': 'success'})

        
class updateTrainStation(APIView):
    def get(self, request):
        for station in TrainStation.objects.all():
            AWSDataForquater.objects.filter(station=station.neareststation, timestamp__gte=timezone.now() - timedelta(days=2)).delete()
            stationdata = AWSDataForquater.objects.filter(station=station.neareststation).order_by('-timestamp')[:4]
            if len(stationdata) == 4:
                rainfall = 0
                for data in stationdata:
                    rainfall += data.rainfall
                if rainfall > 10:
                    station.WarningLevel = 3
                elif rainfall > 5:
                    station.WarningLevel = 2
                elif rainfall > 2.5:
                    station.WarningLevel = 1
                else:
                    station.WarningLevel = 0
            station.save()

        return Response({'status': 'success'})

def updatetrain(station):
    AWSDataForquater.objects.filter(station=station.neareststation, timestamp__gte=timezone.now() - timedelta(days=2)).delete()
    stationdata = AWSDataForquater.objects.filter(station=station.neareststation).order_by('-timestamp')[:4]
    if len(stationdata) == 4:
        rainfall = 0
        for data in stationdata:
            rainfall += data.rainfall
        if rainfall > 10:
            station.WarningLevel = 3
        elif rainfall > 5:
            station.WarningLevel = 2
        elif rainfall > 2.5:
            station.WarningLevel = 1
        else:
            station.WarningLevel = 0
    station.save()

    return Response({'status': 'success'})

    

def health_check(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        return JsonResponse({'status': 'ok'})
    except OperationalError as e:   
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    

class Check(APIView):
    def get(self, request):
        stations = AWSStation.objects.all()
        for station in stations:
            print(station.name)
            data = (
                AWSDataForquater
                .objects
                .filter(
                    station=station, 
                    timestamp__gte=(timezone.now() - timedelta(days=1)).replace(hour=0, minute=0, second=0), 
                    timestamp__lt=(timezone.now() - timedelta(days=1)).replace(hour=23, minute=59, second=59)
                )
                .annotate(hour=TruncHour('timestamp'))
                .values('hour')
                .annotate(total_rainfall=Sum('rainfall'))
                .order_by('hour')
            )

            for d in data:
                StationData.objects.create(
                    station=station,
                    rainfall=d['total_rainfall'],
                    timestamp=datetime.combine((timezone.now() - timedelta(days=1)).date(), d['hour'].time())
                )
                print(station.name, (timezone.now() - timedelta(days=1)).date(), d['hour'].time(), d['total_rainfall'])
        return JsonResponse({'status': 'success'})
