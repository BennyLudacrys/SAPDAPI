from helpers.models import TrackingModel
from django.db import models

from users.models import User


class Person(TrackingModel):
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    nationality = models.CharField(max_length=255, default=None)
    address = models.CharField(max_length=255, blank=True)
    date_of_birth = models.DateTimeField(max_length=255, blank=True)
    last_seen_location = models.CharField(max_length=255, blank=True)
    cellphone = models.CharField(max_length=255, blank=True)
    cellphone1 = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    disease = models.CharField(max_length=255, blank=True)
    picture = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=255, blank=True)
    desc = models.TextField()
    is_complete = models.BooleanField(default=False)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name
