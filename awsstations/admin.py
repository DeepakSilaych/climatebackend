from django.contrib import admin
from .models import AWSStation, DaywisePrediction, TrainStation, StationData, HourlyPrediction

admin.site.register(AWSStation)
admin.site.register(DaywisePrediction)
admin.site.register(TrainStation)
admin.site.register(StationData)
admin.site.register(HourlyPrediction)
