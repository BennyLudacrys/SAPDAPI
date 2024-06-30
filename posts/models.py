from helpers.models import TrackingModel
from django.db import models
from users.models import User
from django.conf import settings


class Post(TrackingModel):
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    nationality = models.CharField(max_length=255, blank=True)
    province = models.CharField(max_length=255, blank=True)
    latitude = models.CharField(max_length=255, blank=True)
    longitude = models.CharField(max_length=255, blank=True)
    gender = models.CharField(max_length=255, blank=True)
    allergies = models.CharField(max_length=255, blank=True)
    medical_conditions = models.CharField(max_length=255, blank=True)
    medications = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)
    block = models.CharField(max_length=255, blank=True)
    neighborhood = models.CharField(max_length=255, blank=True)
    houseNumber = models.CharField(max_length=255, blank=True)
    kinship = models.CharField(max_length=255, blank=True)
    date_of_birth = models.CharField(max_length=255, null=True)
    date_of_disappearance = models.CharField(max_length=255, null=True)
    last_seen_location = models.CharField(max_length=255, blank=True)
    cellphone = models.CharField(max_length=255, blank=True)
    cellphone1 = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    disease = models.CharField(max_length=255, blank=True)
    picture = models.ImageField(upload_to='person_pictures')
    status = models.CharField(max_length=255, blank=True)
    is_complete = models.BooleanField(default=False, blank=True)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='owned_posts', null=True)
    detected_by = models.ManyToManyField(User, related_name='detected_posts', blank=True)

    def __str__(self):
        return self.first_name

    # retornar a contagem de usuários que identificaram o post:
    def get_detected_by_count(self):
        return self.detected_by.count()

    def get_comments_count(self):
        from comments.models import Comment
        return Comment.objects.filter(post=self).count()
