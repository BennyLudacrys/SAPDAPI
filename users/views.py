from django.contrib.auth import authenticate
from rest_framework import response, status, permissions
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, LoginSerializer


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

        if serializer.is_valid():
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