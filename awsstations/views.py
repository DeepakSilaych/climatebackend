
# Create your views here.
from .models import AWSStation, StationData
from .serializers import AWSStationSerializer, StationDataSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models.functions import TruncDate, TruncHour
from django.db.models import Sum



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
        
        now_time = now()

        four_hours_ago = now_time - timedelta(hours=6)
        hourly_data_in_min = StationData.objects.filter(station=station, timestamp__gte=four_hours_ago).order_by('-timestamp').values('timestamp', 'rainfall')
        hourly_data = hourly_data_in_min.annotate(hour=TruncHour('timestamp')).values('hour').annotate(total_rainfall=Sum('rainfall')).order_by('hour')[:5]
        
        three_days_ago = now_time.date() - timedelta(days=3)
        daily_data_in_min = StationData.objects.filter(station=station, timestamp__gte=three_days_ago).order_by('-timestamp').values('timestamp', 'rainfall')
        daily_data = daily_data_in_min.annotate(date=TruncDate('timestamp')).values('date').annotate(total_rainfall=Sum('rainfall')).order_by('date')[:3]     
        return Response({
            'station': serializer.data,
            'hourly_data': hourly_data,
            'daily_data': daily_data
        })


class Test(APIView):
    def get(self, request):
        # download_gfs_data()
        dailyprediction()
        # predict_hourly()
        return Response("Done")