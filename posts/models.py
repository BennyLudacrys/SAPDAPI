from helpers.models import TrackingModel
from django.db import models
from users.models import User


class Post(TrackingModel):
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    nationality = models.CharField(max_length=255, blank=True)
    province = models.CharField(max_length=255, blank=True)
    gender = models.CharField(max_length=255, blank=True)
    allergies = models.CharField(max_length=255, blank=True)
    medical_conditions = models.CharField(max_length=255, blank=True)
    medications = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)
    kinship = models.CharField(max_length=255, blank=True)
    date_of_birth = models.CharField(max_length=255, null=True)
    last_seen_location = models.CharField(max_length=255, blank=True)
    cellphone = models.CharField(max_length=255, blank=True)
    cellphone1 = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    disease = models.CharField(max_length=255, blank=True)
    picture = models.ImageField(upload_to='person_pictures')
    status = models.CharField(max_length=255, blank=True)
    is_complete = models.BooleanField(default=False)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='owned_posts')
    detected_by = models.ManyToManyField(User, related_name='detected_posts')

    def __str__(self):
        return self.first_name

    # retornar a contagem de usuários que identificaram o post:
    def get_detected_by_count(self):
        return self.detected_by.count()
