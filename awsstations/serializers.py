from rest_framework import serializers
from .models import AWSStation, StationData, DaywisePrediction, HourlyPrediction

class AWSStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AWSStation
        fields = '__all__'

class StationDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = StationData
        fields = 'rainfall', 'timestamp'

class DaywisePredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DaywisePrediction
        fields = [ 'day1_rainfall', 'day2_rainfall', 'day3_rainfall']

class HourlyPredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HourlyPrediction
        fields = ['hr_24_rainfall']