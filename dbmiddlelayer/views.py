from django.shortcuts import render
from awsstations.models import *
from awsstations.serializers import *
from crowdsource.models import *
from crowdsource.serializers import *

from rest_framework.views import APIView
from rest_framework.response import Response

# Create your api to access database for each model

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
            rainfall=request.data['rainfall'], 
            temperature=request.data['temperature'], 
            humidity=request.data['humidity'], 
            wind_speed=request.data['wind_speed']
        )
        return Response({'status': 'success'})
    
    def get(self, request):
        station = request.GET.get('station', None)
        if station is not None:
            stationdata = StationData.objects.filter(station=station).order_by('-timestamp')[:100]
        else:
            stationdata = StationData.objects.all().order_by('-timestamp')[:100]
        serializer = StationDataSerializer(stationdata, many=True)
        return Response(serializer.data)

class DaywisePredictionListView(APIView):
    def post(self, request):
        DaywisePrediction.objects.create(
            station=AWSStation.objects.get(station_id=request.data['station']),
            day1_rainfall=request.data['day1'],
            day2_rainfall=request.data['day2'],
            day3_rainfall=request.data['day3']
        )

        return Response({'status': 'success'})

class HourlyPredictionListView(APIView):
    def post(self, request):
        HourlyPrediction.objects.create(
            station=AWSStation.objects.get(station_id=request.data['station']),
            hr_24_rainfall=request.data['hr_24_rainfall']
        )

        
class updateTrainStation(APIView):
    def get(self, request):
        for station in TrainStation.objects.all():
            stationdata = StationData.objects.filter(station=station.neareststation).order_by('-timestamp')[:4]
            if len(stationdata) == 4:
                rainfall = 0
                for data in stationdata:
                    rainfall += data.rainfall
                if rainfall > 100:
                    station.WarningLevel = 3
                elif rainfall > 50:
                    station.WarningLevel = 2
                elif rainfall > 25:
                    station.WarningLevel = 1
                else:
                    station.WarningLevel = 0
            station.save()
        return Response({'status': 'success'})
