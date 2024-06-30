from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Post
from comments.serializers import CommentSerializer


class PersonSerializer(ModelSerializer):
    owner_first_name = serializers.CharField(source='owner.first_name', read_only=True)
    owner_last_name = serializers.CharField(source='owner.last_name', read_only=True)
    owner_picture = serializers.ImageField(source='owner.picture', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post

        fields = ('id', 'created_at', 'updated_at', 'first_name', 'last_name', 'nationality', 'latitude', 'longitude',
                  'address', 'block',
                  'neighborhood', 'houseNumber', 'date_of_birth', 'date_of_disappearance', 'last_seen_location',
                  'cellphone', 'cellphone1', 'description', 'disease', 'picture', 'status', 'is_complete',
                  'owner_first_name', 'owner_last_name', 'kinship', 'province', 'gender', 'allergies',
                  'medical_conditions', 'medications', 'owner_picture', 'comments')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['picture'] = instance.picture.url  # Obter a URL da imagem sem duplicações
        return representation

