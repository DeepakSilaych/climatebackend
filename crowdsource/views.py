from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CSFormData
from .serializers import CSFormSerializer
from .utils import geolocate_text

class StoreData(APIView):
    def post(self, request):
        serializer = CSFormSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            if data.get('latitude') == 0 or data.get('longitude') == 0:
                if data.get('location') is None:
                    return Response({'error': 'Location is required'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    latitude, longitude = geolocate_text(data.get('location'))
                    if latitude is None or longitude is None:
                        return JsonResponse({'error': 'Invalid location'}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        data['latitude'] = latitude
                        data['longitude'] = longitude
            serializer.save()
            return JsonResponse({'message': 'Data stored successfully'}, status=status.HTTP_201_CREATED)
        # try:
        #     print(request.data)
        #     serializer = CSFormSerializer(data=request.data)
        #     if serializer.is_valid():
        #         data = serializer.validated_data
        #         if data.get('latitude') == 0 or data.get('longitude') == 0:
        #             if data.get('location') is None:
        #                 return JsonResponse({'error': 'Location is required'}, status=status.HTTP_400_BAD_REQUEST)
        #             else:
        #                 latitude, longitude = geolocate_text(data.get('location'))
        #                 if latitude is None or longitude is None:
        #                     return JsonResponse({'error': 'Invalid location'}, status=status.HTTP_400_BAD_REQUEST)
        #                 else:
        #                     data['latitude'] = latitude
        #                     data['longitude'] = longitude
        #         serializer.save()
        #         return JsonResponse({'message': 'Data stored successfully'}, status=status.HTTP_201_CREATED)
        #     else:
        #         return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # except Exception as e:
        #     return JsonResponse({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetData(APIView):
    def get(self, request):
        data = CSFormData.objects.all()
        serializer = CSFormSerializer(data, many=True)
        return Response(serializer.data)