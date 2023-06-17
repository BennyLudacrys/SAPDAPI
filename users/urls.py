from django.urls import path, re_path
from . import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('register', views.RegisterAPIView.as_view(), name='register'),
    path('login', views.LoginAPIView.as_view(), name='login'),
    path('user', views.AuthUserAPIView.as_view(), name='user')
    ]
    # re_path(r'users$', views.userApi),
    # re_path(r'users/([0-9]+)$', views.userApi),
    #
    # re_path(r'^users/savefile', views.SaveFile),

    # re_path(r'person$', views.personApi),
    # re_path(r'person/([0-9]+)$', views.personApi),

    # re_path(r'^users/savefile', views.SaveFile),

# ]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
