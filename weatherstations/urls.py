
from django.urls import path
from . import views

urlpatterns = [
    path('stations/', views.WeatherStationListView.as_view()),
    path('station/<int:station_id>/', views.WeatherStationDetailView.as_view()),
    path('sensorlist/', views.FetchSensorList.as_view()),
    path('waterleveldata/<int:thing_id>/', views.FetchWaterLevelData.as_view()),

]