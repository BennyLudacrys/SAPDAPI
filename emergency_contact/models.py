from django.db import models


class Emergency(models.Model):
    entity = models.CharField(max_length=200, blank=True)
    type = models.CharField(max_length=200, blank=True)
    address = models.CharField(max_length=255)
    contact = models.CharField(max_length=50)
    province = models.CharField(max_length=50)

    def __str__(self):
        return self.entity


