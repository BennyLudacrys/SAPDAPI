import cloudinary
from cloudinary.uploader import upload
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import authenticate
from rest_framework import response, status, permissions
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, LoginSerializer, UpdateUserSerializer

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'drxn8xsyi',
    'API_KEY': '785413883832964',
    'API_SECRET': 'FOiok4tpbRm3obrJ56EintpBlG8'
}

cloudinary.config(
    cloud_name=CLOUDINARY_STORAGE['CLOUD_NAME'],
    api_key=CLOUDINARY_STORAGE['API_KEY'],
    api_secret=CLOUDINARY_STORAGE['API_SECRET']
)


class AuthUserAPIView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        serializer = RegisterSerializer(user)

        return response.Response(serializer.data)


class RegisterAPIView(GenericAPIView):
    authentication_classes = []
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        image_file = self.request.data.get('picture')

        if serializer.is_valid():
            if image_file:
                cloudinary_response = cloudinary_upload(image_file, folder='photos')
                if cloudinary_response and 'secure_url' in cloudinary_response:
                    picture_url = cloudinary_response['secure_url']

                    picture_url = picture_url.split("photos/")[-1]
                    serializer.validated_data['picture'] = picture_url

            serializer.save()
            message = "Registro bem-sucedido."
            data = {
                'message': message,
                'data': serializer.data
            }
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(GenericAPIView):
    authentication_classes = []
    serializer_class = LoginSerializer

    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        user = authenticate(username=email, password=password)

        if user:
            serializer = self.serializer_class(user)

            # Gerar um novo refresh token
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return response.Response({'access_token': access_token, **serializer.data}, status=status.HTTP_200_OK)

        return response.Response({'message': "Credenciais inválidas, tente novamente"},
                                 status=status.HTTP_401_UNAUTHORIZED)


def cloudinary_upload(image_file, folder):
    try:
        cloudinary_response = upload(image_file, folder=folder)
        return cloudinary_response
    except Exception as e:
        # Tratar erros de upload aqui
        print("Erro ao fazer upload para o Cloudinary:", e)
        return None


class UpdateUserAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        image_file = request.data.get('picture')
        if image_file:
            cloudinary_response = cloudinary_upload(image_file, folder='photos')
            if cloudinary_response and 'secure_url' in cloudinary_response:
                picture_url = cloudinary_response['secure_url']

                picture_url = picture_url.split("photos/")[-1]
                serializer.validated_data['picture'] = picture_url
        else:
            # Se nenhuma nova imagem for fornecida, mantenha a imagem existente
            serializer.validated_data['picture'] = instance.picture

        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return response.Response(serializer.data)