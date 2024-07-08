from django.urls import path
from .views import StoreData, GetData, GetLocation, TweetMap, Tweet

urlpatterns = [
    path('data/', StoreData.as_view(), name='store_data'),
    path('map/',GetData.as_view(), name='get_data'),
    path('location/', GetLocation.as_view(), name='get_location'),

    path('tweetmap/', TweetMap.as_view(), name='tweetmap'),
    path('tweet/', Tweet.as_view(), name='tweet'),
]
     