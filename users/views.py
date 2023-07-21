from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import response, status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import RegisterSerializer, LoginSerializer
import cloudinary


class AuthUserAPIView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        serializer = RegisterSerializer(user)
        return response.Response({'user': serializer.data})


class RegisterAPIView(GenericAPIView):
    authentication_classes = []
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            message = "Registro bem-sucedido."  # Mensagem personalizada
            data = {
                'message': message,
                'data': serializer.data
            }
            return response.Response(data, status=status.HTTP_201_CREATED)
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
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        return response.Response({'message': "Credenciais invalidas, tente novamente"},
                                 status=status.HTTP_401_UNAUTHORIZED)

#
# @csrf_exempt
# def userApi(request, id=0):
#     if request.method == 'GET':
#         users = User.objects.all()
#         user_serializer = UserSerializer(users, many=True)
#         return JsonResponse(user_serializer.data, safe=False)
#     elif request.method == 'POST':
#         try:
#             user_data = JSONParser().parse(request)
#             user_serializer = UserSerializer(data=user_data)
#             if user_serializer.is_valid():
#                 cloudinary.config(
#                     cloud_name='drxn8xsyi',
#                     api_key='785413883832964',
#                     api_secret='FOiok4tpbRm3obrJ56EintpBlG8'
#                 )
#                 result_upload = cloudinary.uploader.upload(user_serializer.validated_data['picture'])
#                 user = User(
#                     first_name=user_serializer.validated_data['first_name'],
#                     last_name=user_serializer.validated_data['last_name'],
#                     email=user_serializer.validated_data['email'],
#                     cellphone=user_serializer.validated_data['cellphone'],
#                     address=user_serializer.validated_data['address'],
#                     picture=result_upload['url'],
#                     password=user_serializer.validated_data['password']
#                 )
#                 user.save()
#                 return JsonResponse("Adicionado com sucesso", safe=False)
#             return JsonResponse(user_serializer.errors, status=400)
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=400)
#     elif request.method == 'PUT':
#         user_data = JSONParser().parse(request)
#         try:
#             user = User.objects.get(userId=user_data['userId'])
#         except User.DoesNotExist:
#             return JsonResponse("Usuário não encontrado", status=404)
#         user_serializer = UserSerializer(user, data=user_data)
#         if user_serializer.is_valid():
#             user_serializer.save()
#             return JsonResponse("Atualizado com sucesso", safe=False)
#         return JsonResponse(user_serializer.errors, status=400)
#     elif request.method == 'DELETE':
#         try:
#             user = User.objects.get(userId=id)
#         except User.DoesNotExist:
#             return JsonResponse("Usuário não encontrado", status=404)
#         user.delete()
#         return JsonResponse("Deletado com sucesso", safe=False)
#
#
# @csrf_exempt
# def SaveFile(request):
#     if 'file' not in request.FILES:
#         return JsonResponse("Arquivo não encontrado", status=400)
#     file = request.FILES['file']
#     file_name = cloudinary.uploader.upload(file)['url']
#     return JsonResponse(file_name, safe=False)
#
#
# @api_view(['POST'])
# @permission_classes([AllowAny])
# def login_view(request):
#     try:
#         data = request.data
#         serializer = LoginSerializer(data=data)
#         if serializer.is_valid():
#             email = serializer.data['email']
#             password = serializer.data['password']
#
#             user = authenticate(email=email, password=password)
#
#             if user is None:
#                 return Response({
#                     'status': 400,
#                     'message': 'Senha inválida',
#                     'data': {}
#                 })
#
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#             })
#
#         return Response({
#             'status': 400,
#             'message': 'Algo deu errado',
#             'data': serializer.errors
#         }, status=400)
#     except Exception as e:
#         print(e)
#
#
# @api_view(['POST'])
# def logout_view(request):
#     # Lógica de logout aqui, se necessário
#     return JsonResponse({'message': 'Logout realizado com sucesso'})


# @csrf_exempt
# def personApi(request, id=0):
#     if request.method == 'GET':
#         person = Person.objects.all()
#         person_serializer = PersonSerializer(person, many=True)
#         return JsonResponse(person_serializer.data, safe=False)
#     elif request.method == 'POST':
#         try:
#             person_data = JSONParser().parse(request)
#             person_serializer = PersonSerializer(data=person_data)
#             if person_serializer.is_valid():
#                 cloudinary.config(
#                     cloud_name='drxn8xsyi',
#                     api_key='785413883832964',
#                     api_secret='FOiok4tpbRm3obrJ56EintpBlG8'
#                 )
#                 result_upload = cloudinary.uploader.upload(person_serializer.validated_data['picture'])
#                 person = Person(
#                     name=person_serializer.validated_data['name'],
#                     last_name=person_serializer.validated_data['last_name'],
#                     nationality=person_serializer.validated_data['nationality'],
#                     address=person_serializer.validated_data['address'],
#                     date_of_birth=person_serializer.validated_data['date_of_birth'],
#                     last_seen_location=person_serializer.validated_data['last_seen_location'],
#                     cellphone=person_serializer.validated_data['cellphone'],
#                     cellphone1=person_serializer.validated_data['cellphone1'],
#                     description=person_serializer.validated_data['description'],
#                     disease=person_serializer.validated_data['disease'],
#                     picture=result_upload['url'],
#                     status=person_serializer.validated_data['status']
#                 )
#
#                 person.save()
#                 return JsonResponse("Adicionado com sucesso", safe=False)
#             return JsonResponse(person_serializer.errors, status=400)
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=400)
#     elif request.method == 'PUT':
#         user_data = JSONParser().parse(request)
#         try:
#             user = User.objects.get(userId=user_data['userId'])
#         except User.DoesNotExist:
#             return JsonResponse("Usuário não encontrado", status=404)
#         user_serializer = UserSerializer(user, data=user_data)
#         if user_serializer.is_valid():
#             user_serializer.save()
#             return JsonResponse("Atualizado com sucesso", safe=False)
#         return JsonResponse(user_serializer.errors, status=400)
#     elif request.method == 'DELETE':
#         try:
#             user = User.objects.get(userId=id)
#         except User.DoesNotExist:
#             return JsonResponse("Usuário não encontrado", status=404)
#         user.delete()
#         return JsonResponse("Deletado com sucesso", safe=False)
