from django.contrib import admin
from .models import AWSStation, DaywisePrediction, TrainStation, StationData

admin.site.register(AWSStation)
admin.site.register(DaywisePrediction)
admin.site.register(TrainStation)
admin.site.register(StationData)
