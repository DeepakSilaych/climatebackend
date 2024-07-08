from django.db import models

# Create your models here.

class Logs(models.Model):
    log_id = models.AutoField(primary_key=True)
    log = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.log