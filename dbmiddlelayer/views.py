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
        serializer = StationDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class DaywisePredictionListView(APIView):
    def post(self, request):
        serializer = DaywisePredictionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class HourlyPredictionListView(APIView):
    def post(self, request):
        serializer = HourlyPredictionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

        
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
