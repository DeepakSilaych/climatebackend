from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import WeatherStation
from .serializers import WeatherStationSerializer

# Create your views here.

class WeatherStationListView(APIView):
    def get(self, request):
        stations = WeatherStation.objects.all()
        serializer = WeatherStationSerializer(stations, many=True)
        return Response(serializer.data)