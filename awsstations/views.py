
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
    
# class SeasonalStationDataView(APIView):
#     def get(self, request, station_id):
#         # after 10 june
#         stationdata = StationData.objects.filter(station=AWSStation.objects.get(station_id=station_id), timestamp__gte='2021-06-10').order_by('timestamp').values('timestamp', 'rainfall')
#         seasonaldata = stationdata.annotate(date=TruncDate('timestamp')).values('date').annotate(total_rainfall=Sum('rainfall')).order_by('date')
#         return Response(seasonaldata)

class StationDetailView(APIView):
    def get(self, request, station_id):
        station = AWSStation.objects.get(station_id=station_id)
        serializer = AWSStationSerializer(station)

        now_time = pd.Timestamp.now(tz='Asia/Kolkata')

# -----------------------1
        four_hours_ago = now_time - timedelta(hours=6)
        hrly_data_min = StationData.objects.filter(station=station, timestamp__gte=four_hours_ago).order_by('-timestamp').values('timestamp', 'rainfall')
        hrly_data = hrly_data_min.annotate(hour=TruncHour('timestamp')).values('hour').annotate(total_rainfall=Sum('rainfall')).order_by('hour')[:6]
        hrly_data = list(hrly_data)

        pred_hrly = HourlyPrediction.objects.filter(station=station).latest('timestamp')
        update_hrly_data = []

        for i in range(len(hrly_data)):
            update_hrly_data.append({
                'hour': str((now_time.hour - 6 + i)%24)+":00",
                'total_rainfall': hrly_data[i]['total_rainfall']
            })

        index = 0
        for hour, rainfall in pred_hrly.hr_24_rainfall.items():
            update_hrly_data.append({
                'hour': str((now_time.hour + index)%24)+":00",
                'total_rainfall': rainfall  
            })

            index += 1

# -----------------------2
        three_days_ago = now_time.date() - timedelta(days=3)
        daily_data_in_min = StationData.objects.filter(station=station, timestamp__gte=three_days_ago).order_by('-timestamp').values('timestamp', 'rainfall')
        daily_data = daily_data_in_min.annotate(date=TruncDate('timestamp')).values('date').annotate(total_rainfall=Sum('rainfall')).order_by('date')[ :4]
        pred_daily_data = DaywisePrediction.objects.filter(station=station).latest('timestamp')

        update_daily_data = {}
        if pred_daily_data.timestamp.date() == now_time.date():
            for i in [1, 2, 3]:
                update_daily_data[str(daily_data[i]['date'])] = daily_data[i]['total_rainfall']

            update_daily_data [str(now_time.date() + timedelta(days=1))] = pred_daily_data.day1_rainfall
            update_daily_data [str(now_time.date() + timedelta(days=2))] = pred_daily_data.day2_rainfall
            update_daily_data [str(now_time.date() + timedelta(days=3))] = pred_daily_data.day3_rainfall
        
        else :
            for i in [0, 1, 2]:
                update_daily_data[str(daily_data[i]['date'])] = daily_data[i]['total_rainfall']
        
            update_daily_data [str(now_time.date() + timedelta(days=0))] = pred_daily_data.day1_rainfall
            update_daily_data [str(now_time.date() + timedelta(days=1))] = pred_daily_data.day2_rainfall
            update_daily_data [str(now_time.date() + timedelta(days=2))] = pred_daily_data.day3_rainfall
        
# ---------------------- 3
        stationdata = StationData.objects.filter(station=AWSStation.objects.get(station_id=station_id), timestamp__gte='2021-06-10').order_by('timestamp').values('timestamp', 'rainfall')
        seasonaldata = stationdata.annotate(date=TruncDate('timestamp')).values('date').annotate(total_rainfall=Sum('rainfall')).order_by('date')




        return Response({
            'station': serializer.data,
            'hrly_data': update_hrly_data,
            'daily_data': update_daily_data,
            'seasonal_data': seasonaldata
        })
