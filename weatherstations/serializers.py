
from rest_framework import serializers
from .models import WeatherStation, Waterlevel_Data

class WeatherStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherStation
        fields = '__all__'
        
class WaterLevelDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Waterlevel_Data
        fields = ['station', 'waterlevel', 'timestamp']