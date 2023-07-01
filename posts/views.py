from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import PersonSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Person


class PersonListAPIView(ListCreateAPIView):
    serializer_class = PersonSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Person.objects.filter(owner=self.request.user)


class PersonDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = PersonSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'

    def get_queryset(self):
        return Person.objects.filter(owner=self.request.user)
