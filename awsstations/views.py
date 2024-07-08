
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
        stations = AWSStation.objects.all().order_by('name')
        serializer = AWSStationSerializer(stations, many=True)
        return Response(serializer.data)

class TrainStationListView(APIView):
    def get(self, request):
        stations = TrainStation.objects.all()
        serializer = TrainStationSerializer(stations, many=True)
        return Response(serializer.data)
    

class StationDetailView(APIView):
    def get(self, request, station_id):
        now_time = timezone.now()

        # Fetch station and serialize it
        station = AWSStation.objects.get(station_id=station_id)
        serializer = AWSStationSerializer(station).data

        # Fetch hourly data for the last 6 hours and pred for next 24 hours
        pred_hrly_data = HourlyPrediction.objects.filter(station=station).latest('timestamp')
        hrly_data = StationData.objects.filter(station=station).annotate(hour=TruncHour('timestamp')).values('hour').annotate(total_rainfall=Sum('rainfall')).order_by('hour').reverse()[:6]

        # print(hrly_data)
    

        update_hrly_data = [
            {
                'hour': (now_time - timedelta(hours=(6 - i))).strftime('%H:00'),
                'total_rainfall': data['total_rainfall']
            }
            for i, data in enumerate(hrly_data)
        ] + [
            {
                'hour': (now_time + timedelta(hours=i)).strftime('%H:00'),
                'total_rainfall': float(pred_hrly_data.hr_24_rainfall[i])
            }   
            for i in range(24)
        ]

        # print(update_hrly_data)

        # Fetch daily data for the last 4 days
        three_days_ago = now_time.date() - timedelta(days=3)
        daily_data = (
            StationData.objects
            .filter(station=station)
            .annotate(date=TruncDate('timestamp'))
            .values('date')
            .annotate(total_rainfall=Sum('rainfall'))
            .order_by('date')
            .reverse()[:4]
        )

        pred_daily_data = DaywisePrediction.objects.filter(station=station).latest('timestamp') 

        print(pred_daily_data, "----------------------------------------------------------------------")


        try :
            update_daily_data = [
                {
                    'date': str(data['date']) ,
                    'predicted': DaywisePrediction.objects.filter(station=station, timestamp__date=data['date']-timedelta(days=1)).first().day1_rainfall if DaywisePrediction.objects.filter(station=station, timestamp__date=data['date']-timedelta(days=1)) else 0,
                    'observed': data['total_rainfall']
                } for data in (daily_data[:3] if pred_daily_data.timestamp.date() != now_time.date() else daily_data[1:])
            ] + [
                {
                    'date': (now_time.date() + timedelta(days=i)).strftime('%Y-%m-%d') if pred_daily_data.timestamp.date() == now_time.date() else (now_time.date() + timedelta(days=i-1)).strftime('%Y-%m-%d'),
                    'predicted': getattr(pred_daily_data, f'day{i}_rainfall', 0),
                    'observed': 0

                } for i in [1,2,3]
            ]
        except Exception as e:
            print(e)
            update_daily_data = []

        try: 
            mobile_daily_data = {}
            if pred_daily_data :
                if now_time.date() == pred_daily_data.timestamp.date():
                    for data in daily_data[1:]:
                        mobile_daily_data[str(data['date'])] = data['total_rainfall']
            else :
                for data in daily_data[:3]:
                    mobile_daily_data[str(data['date'])] = data['total_rainfall']
                mobile_daily_data[str(now_time.date())] = 0
            
            if now_time.date() == pred_daily_data.timestamp.date() if pred_daily_data else False:
                mobile_daily_data[(now_time.date() + timedelta(days=1)).strftime('%Y-%m-%d')] = pred_daily_data.day1_rainfall
                mobile_daily_data[(now_time.date() + timedelta(days=2)).strftime('%Y-%m-%d')] = pred_daily_data.day2_rainfall
                mobile_daily_data[(now_time.date() + timedelta(days=3)).strftime('%Y-%m-%d')] = pred_daily_data.day3_rainfall
            else:
                mobile_daily_data[now_time.date().strftime('%Y-%m-%d')] = 0
                mobile_daily_data[(now_time.date() + timedelta(days=0)).strftime('%Y-%m-%d')] = pred_daily_data.day1_rainfall
                mobile_daily_data[(now_time.date() + timedelta(days=1)).strftime('%Y-%m-%d')] = pred_daily_data.day2_rainfall
                mobile_daily_data[(now_time.date() + timedelta(days=2)).strftime('%Y-%m-%d')] = pred_daily_data.day3_rainfall
        except Exception as e:
            print(e)
            mobile_daily_data = {}


        # Fetch seasonal data
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
            'seasonal_data': seasonaldata,
            'mobile_daily_data': mobile_daily_data
        })

        # except AWSStation.DoesNotExist:
        #     return Response({'error': 'Station does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        # except DaywisePrediction.DoesNotExist:
        #     return Response({'error': 'Daywise prediction does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        # except IndexError as e:
        #     return Response({'error': f'Index error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # except Exception as e:
        #     return Response({'error': f'Server error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)