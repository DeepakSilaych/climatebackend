from django.urls import path
from .views import StoreData, GetData

urlpatterns = [
    path('data/', StoreData.as_view(), name='store_data'),
    path('map/',GetData.as_view(), name='get_data')
]
