
# Create your views here.
from .models import AWSStation, StationData, DaywisePrediction, HourlyPrediction
from .serializers import AWSStationSerializer, StationDataSerializer, DaywisePredictionSerializer, HourlyPredictionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models.functions import TruncDate, TruncHour
from django.db.models import Sum



import pandas as pd
from .utils.DayWisePrediction import dailyprediction
from .utils.gfs import download_gfs_data
from .utils.hourly_prediction import predict_hourly

class StationListView(APIView):
    def get(self, request):
        stations = AWSStation.objects.all()
        serializer = AWSStationSerializer(stations, many=True)
        return Response(serializer.data)

from django.utils.timezone import now, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers

class AWSStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AWSStation
        fields = '__all__'

class StationDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = StationData
        fields = '__all__'

class StationDetailView(APIView):
    def get(self, request, station_id):
        station = AWSStation.objects.get(station_id=station_id)
        serializer = AWSStationSerializer(station)
        
        now_time = pd.Timestamp.now(tz='Asia/Kolkata')

        four_hours_ago = now_time - timedelta(hours=6)

        hourly_data_in_min = StationData.objects.filter(station=station, timestamp__gte=four_hours_ago).order_by('-timestamp').values('timestamp', 'rainfall')
        hourly_data = hourly_data_in_min.annotate(hour=TruncHour('timestamp')).values('hour').annotate(total_rainfall=Sum('rainfall')).order_by('hour')[:6]

        # add future timestamp to hourly_data
        pred_hrly = HourlyPrediction.objects.filter(station=station).latest('timestamp')
        updated_hrly_data = []
        for i in range(6):
            updated_hrly_data.append({
                'hour': str((now_time.hour - 6 + i)%24)+":00",
                'total_rainfall': hourly_data[i]['total_rainfall']
            })
        for i in range(24):
            updated_hrly_data.append({
                'hour': str((now_time.hour + i)%24)+":00",
                'total_rainfall': pred_hrly.hr_24_rainfall[str(i)]
            })  
        
        three_days_ago = now_time.date() - timedelta(days=3)
        daily_data_in_min = StationData.objects.filter(station=station, timestamp__gte=three_days_ago).order_by('-timestamp').values('timestamp', 'rainfall')
        daily_data = daily_data_in_min.annotate(date=TruncDate('timestamp')).values('date').annotate(total_rainfall=Sum('rainfall')).order_by('date')

        pred_daily_data = DaywisePrediction.objects.filter(station=station).latest('timestamp')
        updated_daily_data = {
            str(daily_data[0]['date']): pred_daily_data.day1_rainfall,
            str(daily_data[1]['date']): pred_daily_data.day2_rainfall,
            str(daily_data[2]['date']): pred_daily_data.day3_rainfall,
            str(now_time.date() + timedelta(days=0)): pred_daily_data.day1_rainfall,
            str(now_time.date() + timedelta(days=1)): pred_daily_data.day2_rainfall,
            str(now_time.date() + timedelta(days=2)): pred_daily_data.day3_rainfall,
        }

        return Response({
            'station': serializer.data,

            'hrly_data': updated_hrly_data,
            'daily_data': updated_daily_data,
        })

