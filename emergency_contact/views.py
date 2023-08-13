from rest_framework import viewsets
from .models import Emergency
from .serializers import EmergencySerializer


class EmergencyContactViewSet(viewsets.ModelViewSet):
    serializer_class = EmergencySerializer

    def get_queryset(self):
        province = self.request.query_params.get('province', None)
        if province is not None:
            queryset = Emergency.objects.filter(province=province)
        else:
            queryset = Emergency.objects.all()
        return queryset
