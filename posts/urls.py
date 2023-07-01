from .views import PersonListAPIView, PersonDetailAPIView
from django.urls import path

urlpatterns = [
    path('', PersonListAPIView.as_view(), name="list-posts"),
    path('<int:id>', PersonDetailAPIView.as_view(), name="detail-post")

]
