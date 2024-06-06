from django.contrib import admin
from .models import WeatherStation, Waterlevel_Data

admin.site.register(WeatherStation)
admin.site.register(Waterlevel_Data)
