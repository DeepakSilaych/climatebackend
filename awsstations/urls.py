# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('stations/', views.StationListView.as_view()),
    path('stations/<int:station_id>/', views.StationDetailView.as_view()),
    path('predictions/', views.get_predictions),    
]
