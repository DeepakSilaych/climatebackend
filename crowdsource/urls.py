from django.urls import path
from .views import StoreData, GetData, GetLocation, FetchSensorList, FetchWaterLevelData, TweetMap, Tweet

urlpatterns = [
    path('data/', StoreData.as_view(), name='store_data'),
    path('map/',GetData.as_view(), name='get_data'),
    path('location/', GetLocation.as_view(), name='get_location'),

    path('tweetmap/', TweetMap.as_view(), name='tweetmap'),
    path('tweet/', Tweet.as_view(), name='tweet'),

    path('sensorlist/', FetchSensorList.as_view(), name='fetchsensorlist'),
    path('waterleveldata/<int:thing_id>/', FetchWaterLevelData.as_view(), name='fetchwaterleveldata'),
]
