
# Create your views here.
from .models import AWSStation, StationData, DaywisePrediction, HourlyPrediction, TrainStation
from .serializers import AWSStationSerializer, TrainStationSerializer ,StationDataSerializer, DaywisePredictionSerializer, HourlyPredictionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models.functions import TruncDate, TruncHour
from django.db.models import Sum
from rest_framework import status 
from django.utils.timezone import now, timedelta
import pandas as pd
from django.utils.timezone import make_aware
from datetime import datetime
from django.utils import timezone


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
        try:
            now_time = timezone.now()

            # Fetch station and serialize it
            station = AWSStation.objects.get(station_id=station_id)
            serializer = AWSStationSerializer(station).data

            # Fetch hourly data for the last 6 hours and pred for next 24 hours
            four_hours_ago = now_time - timedelta(hours=6)
            pred_hrly_data = HourlyPrediction.objects.filter(station=station).latest('timestamp')
            hrly_data = (
                StationData.objects
                .filter(station=station, timestamp__gte=four_hours_ago)
                .annotate(hour=TruncHour('timestamp'))
                .values('hour')
                .annotate(total_rainfall=Sum('rainfall'))
                .order_by('hour')[:6]
            )

            update_hrly_data = [
                {
                    'hour': (now_time - timedelta(hours=(6 - i))).strftime('%H:00'),
                    'total_rainfall': data['total_rainfall']
                }
                for i, data in enumerate(hrly_data)
            ] + [
                {
                    'hour': (now_time + timedelta(hours=i)).strftime('%H:00'),
                    'total_rainfall': pred_hrly_data.hr_24_rainfall.get(str(i), 0)
                }
                for i in range(24)
            ]

            # Fetch daily data for the last 4 days
            three_days_ago = now_time.date() - timedelta(days=4)
            daily_data = (
                StationData.objects
                .filter(station=station, timestamp__gte=three_days_ago)
                .annotate(date=TruncDate('timestamp'))
                .values('date')
                .annotate(total_rainfall=Sum('rainfall'))
                .order_by('date')[:4]
            )

            pred_daily_data = DaywisePrediction.objects.filter(station=station).latest('timestamp')
            update_daily_data = {}

            for i, data in enumerate(daily_data):
                update_daily_data[str(data['date'])] = data['total_rainfall']

            for i in [1,2,3]:
                day = now_time.date() + timedelta(days=i)
                if pred_daily_data.timestamp.date() == day:
                    update_daily_data[str(day)] = getattr(pred_daily_data, f'day{i+1}_rainfall', 0)
                else:
                    update_daily_data[str(day)] = getattr(pred_daily_data, f'day{i+1}_rainfall', 0)

            # Fetch seasonal data (observed and predicted)
            stationdata = (
                StationData.objects
                .filter(station=station, timestamp__gte='2021-06-10')
                .annotate(date=TruncDate('timestamp'))
                .values('date')
                .annotate(total_rainfall=Sum('rainfall'))
                .order_by('date')
            )

            seasonaldata = []
            for data in stationdata:
                previous_day = data['date'] - timedelta(days=1)
                predicted_rainfall = DaywisePrediction.objects.filter(station=station, timestamp__date=previous_day).first()
                predicted_value = predicted_rainfall.day1_rainfall if predicted_rainfall else 0
                seasonaldata.append({
                    'date': data['date'],
                    'observed': data['total_rainfall'],
                    'predicted': predicted_value
                })

            return Response({
                'station': serializer,
                'hrly_data': update_hrly_data,
                'daily_data': update_daily_data,
                'seasonal_data': seasonaldata
            })

        except AWSStation.DoesNotExist:
            return Response({'error': 'Station does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        except DaywisePrediction.DoesNotExist:
            return Response({'error': 'Daywise prediction does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        except IndexError as e:
            return Response({'error': f'Index error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            return Response({'error': f'Server error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)