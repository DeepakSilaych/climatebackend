from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CSFormData, Tweets
from .serializers import CSFormSerializer, FormDataSerializer, TweetsSerializer

from .utils import geolocate_text, cord_to_text

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta

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
        

class Tweet(APIView):
    def get(self, request):
        tweets = Tweets.objects.all()
        serializer = TweetsSerializer(tweets, many=True)
        return Response(serializer.data)