from django.db import models


# form data model
class CSFormData(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    waterlevel = models.FloatField()

    location = models.CharField(max_length=100 , blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)

    latitude = models.FloatField()
    longitude = models.FloatField()
# tweet data model

# class Tweet(models.Model):
#     tweet_text = models.CharField(max_length=200)
#     timestamp = models.DateTimeField()
#     sentiment = models.BooleanField()
#     latitude = models.FloatField()
#     longitude = models.FloatField()
#     address = models.CharField()
    
    