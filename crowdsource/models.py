from django.db import models


# form data model
class CSFormData(models.Model):
    
    location = models.TextField(blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)

    feet = models.IntegerField(blank=True, null=True)
    inch = models.IntegerField(blank=True, null=True)

    timestamp = models.DateTimeField(auto_now=True, null=True)

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

    