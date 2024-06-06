from django.db import models
from django.contrib.postgres.fields import ArrayField


class WeatherStation(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    image = models.ImageField(upload_to='weatherstation_images/', blank=True, null=True)

    curr_waterlevel = models.FloatField(default=0)
    arr_waterlevel = ArrayField(base_field=models.FloatField(), size=30)

    def __str__(self):
        return self.name

class Waterlevel_Data(models.Model):
    station = models.ForeignKey(WeatherStation, on_delete=models.CASCADE)

    waterlevel = models.FloatField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.station.name + " " + str(self.timestamp)
