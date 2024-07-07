from django.urls import path
from .views import StoreData, GetData, GetLocation, Tweet, FetchSensorList, FetchWaterLevelData

urlpatterns = [
    path('data/', StoreData.as_view(), name='store_data'),
    path('map/',GetData.as_view(), name='get_data'),
    path('location/', GetLocation.as_view(), name='get_location'),
    path('tweet/', Tweet.as_view()),

    path('sensorlist/', FetchSensorList.as_view(), name='fetchsensorlist'),
    path('waterleveldata/<int:thing_id>/', FetchWaterLevelData.as_view(), name='fetchwaterleveldata'),
]
