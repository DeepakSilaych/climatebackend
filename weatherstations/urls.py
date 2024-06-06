
from django.urls import path
from . import views

urlpatterns = [
    path('stations/', views.WeatherStationListView.as_view()),
    # path('stations/<int:station_id>/', views.WeatherStationDetailView.as_view()),   
]