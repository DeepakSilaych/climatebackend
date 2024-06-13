from django.urls import path
from .views import StoreData, GetData, GetLocation

urlpatterns = [
    path('data/', StoreData.as_view(), name='store_data'),
    path('map/',GetData.as_view(), name='get_data'),
    path('location/', GetLocation.as_view(), name='get_location')
]
