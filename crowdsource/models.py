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

    def __str__(self):
        return self.location + " " + str(self.feet) + "ft " + str(self.inch) + "in"
# tweet data model

class Tweets(models.Model):
    tweet_text = models.TextField()
    timestamp = models.DateTimeField()
    sentiment = models.BooleanField() # True for positive, False for negative
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    address = models.CharField(null=True, max_length=200)

    def __str__(self) -> str:
        return self.tweet_text + str(self.timestamp)

    