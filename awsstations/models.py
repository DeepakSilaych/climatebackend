from django.db import models

class AWSStation(models.Model):
    station_id = models.IntegerField()
    name = models.CharField(max_length=100)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    curr_rainfall = models.FloatField(default=0)
    curr_temp = models.FloatField(default=0)
    curr_windspeed = models.FloatField(default=0)

    def __str__(self):
        return self.name
    

class StationData(models.Model):
    station = models.ForeignKey(AWSStation, on_delete=models.CASCADE)
    rainfall = models.FloatField(default=0)
    temperature = models.FloatField(default=0)
    humidity = models.FloatField(default=0)
    wind_speed = models.FloatField(default=0)
    timestamp = models.DateTimeField()
    
    def __str__(self):
        return self.station.name + " " + str(self.timestamp)
    

class DaywisePrediction(models.Model):
    station = models.ForeignKey(AWSStation, on_delete=models.CASCADE, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    day1_rainfall = models.FloatField(default=0)
    day2_rainfall = models.FloatField(default=0)
    day3_rainfall = models.FloatField(default=0)

    def __str__(self):
        return self.station.name + " " + str(self.timestamp)
    
class HourlyPrediction(models.Model):
    station = models.ForeignKey(AWSStation, on_delete=models.CASCADE, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    hr_24_rainfall = models.JSONField(default=dict)

    def __str__(self):
        return self.station.name + " " + str(self.timestamp)
    


class TrainStation(models.Model):
    station_code = models.IntegerField(primary_key=True)
    station_name = models.CharField(max_length=100)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    neareststation = models.ForeignKey( 'AWSStation' , on_delete=models.CASCADE, blank=True, null=True)
    WarningLevel = models.IntegerField(default=0)

    def __str__(self):
        return self.station_name
    def update(self):
        last_data = StationData.objects.filter(station=self.neareststation).order_by('-timestamp')[:4]
        if last_data:
            max_rainfall = max(data.rainfall for data in last_data)
            if max_rainfall > 20:
                self.WarningLevel = 3
            elif max_rainfall > 15:
                self.WarningLevel = 2
            elif max_rainfall > 10:
                self.WarningLevel = 1
            else:
                self.WarningLevel = 0