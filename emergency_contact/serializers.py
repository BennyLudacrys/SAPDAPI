from rest_framework import serializers
from .models import Emergency


class EmergencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Emergency
        fields = '__all__'


