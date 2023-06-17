from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128, min_length=6, write_only=True
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'last_name', 'first_name', 'address')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128, min_length=6, write_only=True
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'token')
        read_only_fields = ['token']

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('userId', 'first_name', 'last_name', 'email', 'cellphone', 'address', 'picture', 'password')


# class PersonSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Person
#         fields = (
#             'name', 'last_name', 'nationality', 'address', 'date_of_birth', 'last_seen_location', 'cellphone', 'cellphone1', 'description',
#             'disease', 'picture', 'status')


# class LoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField()
