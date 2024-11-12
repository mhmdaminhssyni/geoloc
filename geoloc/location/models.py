from django.db import models
from django.contrib.auth.models import User

class UserGeoLocation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    latitude = models.FloatField(blank=False, null=False)
    longitude = models.FloatField(blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)  # Optional for tracking when the location was saved

    def __str__(self):
        return f"{self.user.username} - {self.timestamp}"
