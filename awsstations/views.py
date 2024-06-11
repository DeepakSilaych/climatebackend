
# Create your views here.
from .models import AWSStation, StationData, DaywisePrediction, HourlyPrediction, TrainStation
from .serializers import AWSStationSerializer, TrainStationSerializer ,StationDataSerializer, DaywisePredictionSerializer, HourlyPredictionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models.functions import TruncDate, TruncHour
from django.db.models import Sum
from django.utils.timezone import now, timedelta
import pandas as pd

class StationListView(APIView):
    def get(self, request):
        stations = AWSStation.objects.all()
        serializer = AWSStationSerializer(stations, many=True)
        return Response(serializer.data)

class TrainStationListView(APIView):
    def get(self, request):
        stations = TrainStation.objects.all()
        serializer = TrainStationSerializer(stations, many=True)
        return Response(serializer.data)

class StationDetailView(APIView):
    def get(self, request, station_id):
        station = AWSStation.objects.get(station_id=station_id)
        serializer = AWSStationSerializer(station)

        print ("------------------------------------------------------------------1")
        
        now_time = pd.Timestamp.now(tz='Asia/Kolkata')

        four_hours_ago = now_time - timedelta(hours=6)

        hourly_data_in_min = StationData.objects.filter(station=station, timestamp__gte=four_hours_ago).order_by('-timestamp').values('timestamp', 'rainfall')
        hourly_data = hourly_data_in_min.annotate(hour=TruncHour('timestamp')).values('hour').annotate(total_rainfall=Sum('rainfall')).order_by('hour')[:6]

        print ("------------------------------------------------------------------2")

        # add future timestamp to hourly_data
        pred_hrly = HourlyPrediction.objects.filter(station=station).latest('timestamp')

        print ("------------------------------------------------------------------3.1")

        updated_hrly_data = []
        if len(hourly_data) < 6:
            for i in range(6 - len(hourly_data)):
                updated_hrly_data.append({
                    'hour': str((now_time.hour - 6 + i)%24)+":00",
                    'total_rainfall': 0
                })
        else :
                
            for i in range(6):
                updated_hrly_data.append({
                    'hour': str((now_time.hour - 6 + i)%24)+":00",
                    'total_rainfall': hourly_data[i]['total_rainfall']
                })

        print ("------------------------------------------------------------------3")
        
        for i in range(24):
            if str(i) in pred_hrly.hr_24_rainfall:
                updated_hrly_data.append({
                    'hour': str((now_time.hour + i)%24)+":00",
                    'total_rainfall': pred_hrly.hr_24_rainfall[str(i)]
                })
            else:
                updated_hrly_data.append({
                    'hour': str((now_time.hour + i)%24)+":00",
                    'total_rainfall': 0  # or some default value
                })
        
        print ("------------------------------------------------------------------4")
        
        three_days_ago = now_time.date() - timedelta(days=3)
        daily_data_in_min = StationData.objects.filter(station=station, timestamp__gte=three_days_ago).order_by('-timestamp').values('timestamp', 'rainfall')
        daily_data = daily_data_in_min.annotate(date=TruncDate('timestamp')).values('date').annotate(total_rainfall=Sum('rainfall')).order_by('date')

        print ("------------------------------------------------------------------5")


        pred_daily_data = DaywisePrediction.objects.filter(station=station).latest('timestamp')
        updated_daily_data = {
            str(daily_data[0]['date']): pred_daily_data.day1_rainfall,
            str(daily_data[1]['date']): pred_daily_data.day2_rainfall,
            str(daily_data[2]['date']): pred_daily_data.day3_rainfall,
            str(now_time.date() + timedelta(days=0)): pred_daily_data.day1_rainfall,
            str(now_time.date() + timedelta(days=1)): pred_daily_data.day2_rainfall,
            str(now_time.date() + timedelta(days=2)): pred_daily_data.day3_rainfall,
        }

        print ("------------------------------------------------------------------6")

        return Response({
            'station': serializer.data,

            'hrly_data': updated_hrly_data,
            'daily_data': updated_daily_data,
        })

