from rest_framework import viewsets
from .models import Emergency
from .serializers import EmergencySerializer


class EmergencyContactViewSet(viewsets.ModelViewSet):
    serializer_class = EmergencySerializer

    def get_queryset(self):
        province = self.request.query_params.get('province', None)
        contact_type = self.request.query_params.get('type', None)

        queryset = Emergency.objects.all()

        if province is not None:
            queryset = queryset.filter(province=province)

        if contact_type is not None:
            queryset = queryset.filter(type=contact_type)

        return queryset
