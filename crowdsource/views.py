from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from .models import CSFormData
from .serializers import CSFormSerializer
from .utils import geolocate_text

class StoreData(APIView):
    def post(self, request):
        try:
            print(request.data)
            serializer = CSFormSerializer(data=request.data)
            if serializer.is_valid():
                data = serializer.validated_data
                if data.get('latitude') == 0 or data.get('longitude') == 0:
                    if data.get('location') is None:
                        return JsonResponse({'error': 'Location is required'}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        latitude, longitude = geolocate_text(data.get('location'))
                        if latitude is None or longitude is None:
                            return JsonResponse({'error': 'Invalid location'}, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            data['latitude'] = latitude
                            data['longitude'] = longitude
                serializer.save()
                return JsonResponse({'message': 'Data stored successfully'}, status=status.HTTP_201_CREATED)
            else:
                return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetData(APIView):
    def get(self, request):
        try:
            queryset = CSFormData.objects.all()
            if not queryset.exists():
                return JsonResponse({'message': 'No data available'}, status=status.HTTP_204_NO_CONTENT)
            data = [{'latitude': obj.latitude, 'longitude': obj.longitude, 'waterlevel': obj.waterlevel} for obj in queryset]
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 