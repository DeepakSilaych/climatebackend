from django.db import models
from awsstations.models import AWSStation

class AWSDataForquater(models.Model):
    station = models.ForeignKey(AWSStation, on_delete=models.CASCADE)
    rainfall = models.FloatField()
    timestamp = models.DateTimeField(auto_now=True)