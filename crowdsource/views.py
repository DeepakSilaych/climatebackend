from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CSFormData, Tweets
from .serializers import CSFormSerializer, FormDataSerializer, TweetsSerializer, TweetsMapSerializer

from .utils import geolocate_text, cord_to_text

from django.utils import timezone
from datetime import timedelta
import requests
import time


class StoreData(APIView):
    def post(self, request):
        data = request.data
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        location = data.get('location')
        feet = data.get('feet')
        inch = data.get('inch')
        feedback = data.get('feedback')

        print(data)

        if latitude is None or longitude is None:
            if location is not None:
                try:
                    lat, long = geolocate_text(location)
                    CSFormData.objects.create(feet=feet, inch=inch, location=location, latitude=lat, longitude=long, feedback=feedback)
                    return Response({'message': 'Data stored successfully'})
                except Exception as e:
                    return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({'error': 'Invalid location'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                CSFormData.objects.create(feet=feet, inch=inch, location=location, latitude=latitude, longitude=longitude, feedback=feedback)
                return Response({'message': 'Data stored successfully'})
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetData(APIView):
    def get(self, request):
        # last 24 hrs data
        data = CSFormData.objects.filter(timestamp__gte=timezone.now()-timedelta(days=1))
        serializer = CSFormSerializer(data, many=True)
        return Response(serializer.data)
    
class GetLocation(APIView):
    def post(self, request):
        latitude = request.data.get('lat')
        longitude = request.data.get('long')
        location = cord_to_text(latitude, longitude)
        if location:
            return Response({'location': location})
        else:
            return Response({'error': 'Invalid coordinates'}, status=status.HTTP_400_BAD_REQUEST) 

class FetchSensorList(APIView):
    def get(self, request):
        access_id = 'lX1d9akADFVLiYhB'
        access_key = 'NsKeyQDu9zgbED9KINEeYhIvRzbcSr1VKtDhbTMaUQMlAtPA8sOyjDm8Q85CBH9d'
        url = 'https://app.aurassure.com/-/api/iot-platform/v1.1.0/clients/10684/applications/16/things/list'

        try:
            response = requests.get(url, headers={
                'Access-Id': access_id,
                'Access-Key': access_key,
                'Content-Type': 'application/json'
            })

            response_data = response.json()
            sensor_list = [
                {
                    'id': sensor['id'],
                    'name': sensor['name'],
                    'latitude': sensor['latitude'],
                    'longitude': sensor['longitude'],
                    'address': sensor['address']
                } for sensor in response_data['things']
            ]
            return Response(sensor_list, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class FetchWaterLevelData(APIView):
    def get(self, request, thing_id):
        access_id = 'lX1d9akADFVLiYhB'
        access_key = 'NsKeyQDu9zgbED9KINEeYhIvRzbcSr1VKtDhbTMaUQMlAtPA8sOyjDm8Q85CBH9d'
        url = 'https://app.aurassure.com/-/api/iot-platform/v1.1.0/clients/10082/applications/16/things/data'

        try:
            now = int(time.time())
            from_time = now - 24 * 60 * 60

            payload = {
                'data_type': 'raw',
                'aggregation_period': 0,
                'parameters': ['us_mb'],
                'parameter_attributes': [],
                'things': [thing_id],
                'from_time': from_time,
                'upto_time': now
            }

            response = requests.post(url, json=payload, headers={
                'Access-Id': access_id,
                'Access-Key': access_key,
                'Content-Type': 'application/json'
            })

            return Response(response.json(), status=status.HTTP_200_OK)
        except requests.RequestException as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TweetMap(APIView):
    def get(self, request):
        # fetch tweet with non-zero latitude and longitude values, is null isnt correct parameter in last 24 hours
        tweets = Tweets.objects.filter(latitude__isnull=False, longitude__isnull=False, timestamp__gte=timezone.now()-timedelta(days=1))
        serializer = TweetsMapSerializer(tweets, many=True)
        return Response(serializer.data)

class Tweet(APIView):
    def get(self, request):
        tweets = Tweets.objects.all().order_by('-timestamp')
        serializer = TweetsSerializer(tweets, many=True)
        return Response(serializer.data)