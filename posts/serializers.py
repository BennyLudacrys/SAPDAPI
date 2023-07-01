from rest_framework.serializers import ModelSerializer
from .models import Person


class PersonSerializer(ModelSerializer):
    class Meta:
        model = Person
        fields = ('id', 'first_name', 'last_name', 'nationality', 'address', 'date_of_birth', 'last_seen_location',
                  'cellphone', 'cellphone1', 'desc', 'disease', 'picture', 'status', 'is_complete')
