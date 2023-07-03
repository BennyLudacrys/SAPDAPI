from rest_framework.serializers import ModelSerializer
from .models import Post


class PersonSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'first_name', 'last_name', 'nationality', 'address', 'date_of_birth', 'last_seen_location',
                  'cellphone', 'cellphone1', 'desc', 'disease', 'picture', 'status', 'is_complete')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['picture'] = instance.picture.url  # Obter a URL da imagem sem duplicações
        return representation
