from django.urls import path
from .views import *

urlpatterns = [
    path('awsstations/', AWSStationListView.as_view()),
    path('stationdata/', StationDataListView.as_view()),
    path('daywiseprediction/', DaywisePredictionListView.as_view()),
    path('hourlyprediction/', HourlyPredictionListView.as_view()),
    path('updatetrainstation/', updateTrainStation.as_view()),

]