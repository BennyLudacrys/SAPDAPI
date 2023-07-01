from .views import PersonListAPIView, PersonDetailAPIView
from django.urls import path

urlpatterns = [
    path('', PersonListAPIView.as_view(), name="list-persons"),
    path('<int:id>', PersonDetailAPIView.as_view(), name="detail-person")

]
