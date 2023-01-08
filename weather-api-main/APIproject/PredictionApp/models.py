from asyncio.windows_events import NULL
from django.db import models
from datetime import datetime
from django.utils import timezone

class Prediction(models.Model):
    email = models.EmailField(
        max_length=255,
        unique=False,
        default=NULL
    )
    postal_code = models.CharField(max_length=8)
    latitude = models.FloatField(default=NULL)
    longitude = models.FloatField(default=NULL)
    date_exec = models.DateTimeField(default= timezone.now)
    nb_days = models.IntegerField(default=NULL)
    data = models.JSONField(default=dict)