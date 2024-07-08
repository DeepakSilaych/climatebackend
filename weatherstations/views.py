from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import WeatherStation, Waterlevel_Data
from .serializers import WeatherStationSerializer

# Create your views here.

class WeatherStationListView(APIView):
    def get(self, request):
        stations = WeatherStation.objects.all()
        serializer = WeatherStationSerializer(stations, many=True)
        return Response(serializer.data)

class WeatherStationDetailView(APIView):
    def get(self, request, station_id):
        station = WeatherStation.objects.get(station_id=station_id)
        data = Waterlevel_Data.objects.filter(station=station).order_by('-timestamp')[:30]
        data = data[::-1]
        serializer = WeatherStationSerializer(station)
        return Response({'station': serializer.data, 'data': data})
    

class FetchSensorList(APIView):
    def get(self, request):
        data = things_list()
        return Response(data)


class FetchWaterLevelData(APIView):
    def get(self, request, thing_id):
        data = thing_data(thing_id)
        return Response(data)
