from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('detect-image/', views.detect_image, name='detect_image'),
]