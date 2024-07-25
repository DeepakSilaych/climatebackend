from django.db import models
from awsstations.models import AWSStation
from django.utils.timezone import now

class AWSDataForquater(models.Model):
    station = models.ForeignKey(AWSStation, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=now)
    rainfall = models.FloatField()
    
    def __str__(self):
        return str(self.station) + ' - ' + str(self.rainfall) + 'mm'
    
    class Meta:
        verbose_name = 'Quater AWS Data'
        verbose_name_plural = 'Quater AWS Data'
        ordering = ['-timestamp']