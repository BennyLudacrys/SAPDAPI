import cloudinary
from cloudinary.uploader import upload as cloudinary_upload
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.models import User

from .models import Post
from .serializers import PersonSerializer

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


class PersonListAPIView(ListCreateAPIView):
    serializer_class = PersonSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [SearchFilter]
    search_fields = ['status']  # Define os campos que podem ser filtrados

    def perform_create(self, serializer):
        image_file = self.request.data.get('picture')

        if image_file:
            cloudinary_response = cloudinary_upload(image_file, folder='photos')
            if cloudinary_response and 'secure_url' in cloudinary_response:
                picture_url = cloudinary_response['secure_url']

                picture_url = picture_url.split("photos/")[-1]
                serializer.save(owner=self.request.user, picture=picture_url)
                return

        serializer.save(owner=self.request.user)

    def get_queryset(self):
        # Filtra os posts do usuário logado com base no status
        queryset = Post.objects.filter(owner=self.request.user, status__in=['encontrado', 'desaparecido'])
        return queryset


class PersonDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = PersonSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'

    def perform_update(self, serializer):
        image_file = self.request.data.get('picture')

        if image_file:
            # Upload da nova imagem para o Cloudinary
            cloudinary_response = cloudinary_upload(image_file)

            if cloudinary_response and 'secure_url' in cloudinary_response:
                picture_url = cloudinary_response['secure_url']

                picture_url = picture_url.split("photos/")[-1]
                serializer.save(picture=picture_url)
                return

        serializer.save()

    def get_queryset(self):
        return Post.objects.filter(owner=self.request.user)

    @api_view(['POST'])
    def change_status(self, post_id):
        try:
            post = get_object_or_404(Post, id=post_id)

            # Verificar se o usuário autenticado é o proprietário do post
            # if post.owner != request.user.username:
            #     return Response({'message': 'You are not authorized to change the status of this post'},
            #                     status=status.HTTP_401_UNAUTHORIZED)

            if post.status == 'Livre':
                post.status = 'Desaparecido'
            if post.status == 'Encontrado':
                post.status = 'Livre'
            elif post.status == 'Livre':
                post.status = 'Desaparecido'
            else:
                return Response({'message': 'Estado Invalido'}, status=status.HTTP_400_BAD_REQUEST)

            post.save()
            return Response({'message': f'Status changed to "{post.status}"'}, status=status.HTTP_200_OK)

        except Post.DoesNotExist:
            return Response({'error': 'Post does not exist'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def change_statuss(request, post_id):
    try:
        post = get_object_or_404(Post, id=post_id)

        # Verificar se o usuário autenticado é o proprietário do post
        # if post.owner != request.user.username:
        #     return Response({'message': 'You are not authorized to change the status of this post'},
        #                     status=status.HTTP_401_UNAUTHORIZED)

        if post.status == 'Desaparecido':
            post.status = 'Livre'
        elif post.status == 'Livre':
            post.status = 'Desaparecido'
        elif post.status == 'Encontrado':
            post.status = 'Livre'
        else:
            return Response({'message': 'Estado invalido'}, status=status.HTTP_400_BAD_REQUEST)

        post.save()
        return Response({'message': f'Status changed to "{post.status}"'}, status=status.HTTP_200_OK)

    except Post.DoesNotExist:
        return Response({'error': 'Post does not exist'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_posts_by_user(request, user_id):
    try:
        user = get_object_or_404(User, id=user_id)
        posts = Post.objects.filter(detected_by=user)

        post_data = []
        for post in posts:
            post_data.append({
                'id': post.id,
                'first_name': post.first_name,
                'last_name': post.last_name,
                "nationality": post.nationality,
                "address": post.address,
                "date_of_birth": post.date_of_birth,
                "last_seen_location": post.last_seen_location,
                "cellphone": post.cellphone,
                "cellphone1": post.cellphone1,
                "description": post.description,
                "disease": post.disease,
                "picture": post.picture.url,
                'owner_picture': owner_picture_url_utf8 if owner_picture_url else None,
                "status": post.status,
                "is_complete": post.is_complete,
                'kinship': post.kinship,
                # 'owner_last_name': post.owner.last_name,

            })

        return Response({'posts': post_data})
    except User.DoesNotExist:
        return Response({'error': 'User does not exist'})


@api_view(['GET'])
def get_post(request, post_id):
    try:
        post = get_object_or_404(Post, id=post_id)
        detected_by_count = post.get_detected_by_count()

        post_data = {
            'id': post.id,
            'created_at': post.created_at,
            'updated_at': post.updated_at,
            'first_name': post.first_name,
            'last_name': post.last_name,
            "nationality": post.nationality,
            "address": post.address,
            "date_of_birth": post.date_of_birth,
            "last_seen_location": post.last_seen_location,
            "cellphone": post.cellphone,
            "cellphone1": post.cellphone1,
            "description": post.description,
            "disease": post.disease,
            "picture": post.picture.url,
            "status": post.status,
            "is_complete": post.is_complete,
            'kinship': post.kinship,
            'province': post.province,
            'gender': post.gender,
            'allergies': post.allergies,
            'medical_conditions': post.medical_conditions,
            'medications': post.medications,
            # 'owner_first_name': post.owner.first_name,
            # 'owner_last_name': post.owner.last_name,
            # Adicione outros campos do modelo Post que você deseja retornar
            'detected_by_count': detected_by_count,
        }

        return Response(post_data)
    except Post.DoesNotExist:
        return Response({'error': 'Post does not exist'})


@api_view(['GET'])
def get_all_posts(request):
    try:
        posts = Post.objects.all()

        post_data = []
        for post in posts:
            owner_picture = post.owner.picture
            owner_picture_url = owner_picture.url if owner_picture and owner_picture.name else None
            owner_picture_url_utf8 = owner_picture_url.encode('utf-8').decode('utf-8') if owner_picture_url else None
            post_data.append({
                'id': post.id,
                'created_at': post.created_at,
                'updated_at': post.updated_at,
                'first_name': post.first_name,
                'last_name': post.last_name,
                "nationality": post.nationality,
                "address": post.address,
                "date_of_birth": post.date_of_birth,
                "last_seen_location": post.last_seen_location,
                "cellphone": post.cellphone,
                "cellphone1": post.cellphone1,
                "description": post.description,
                "disease": post.disease,
                "picture": owner_picture_url_utf8,
                "status": post.status,
                'kinship': post.kinship,
                "is_complete": post.is_complete,
                'owner_first_name': post.owner.first_name,
                'owner_last_name': post.owner.last_name,
                'owner_picture': owner_picture_url_utf8 if owner_picture_url else None,
                'province': post.province,
                'gender': post.gender,
                'allergies': post.allergies,
                'medical_conditions': post.medical_conditions,
                'medications': post.medications,
            })

        return Response(post_data)
    except Post.DoesNotExist:
        return Response({'error': 'Nenhum Post foi Encontrado'})


@api_view(['GET'])
def get_posts_by_status(request):
    try:
        status_params = ['Desaparecido', 'Encontrado']

        posts = Post.objects.filter(status__in=status_params)

        post_data = []
        for post in posts:
            owner_picture = post.owner.picture
            owner_picture_url = owner_picture.url if owner_picture and owner_picture.name else None
            owner_picture_url_utf8 = owner_picture_url.encode('utf-8').decode('utf-8') if owner_picture_url else None
            post_data.append({
                'id': post.id,
                'created_at': post.created_at,
                'updated_at': post.updated_at,
                'first_name': post.first_name,
                'last_name': post.last_name,
                "nationality": post.nationality,
                "address": post.address,
                "date_of_birth": post.date_of_birth,
                "last_seen_location": post.last_seen_location,
                "cellphone": post.cellphone,
                "cellphone1": post.cellphone1,
                "description": post.description,
                "disease": post.disease,
                'kinship': post.kinship,
                'province': post.province,
                'gender': post.gender,
                'allergies': post.allergies,
                'medical_conditions': post.medical_conditions,
                'owner_picture': owner_picture_url_utf8 if owner_picture_url else None,
                'medications': post.medications,
                "picture": post.picture.url,
                "status": post.status,
                "is_complete": post.is_complete,
                'owner_first_name': post.owner.first_name,
                'owner_last_name': post.owner.last_name,
            })

        return Response(post_data)
    except Post.DoesNotExist:
        return Response({'error': 'No posts found'})


@api_view(['GET'])
def get_free_posts(request):
    try:
        status_param = 'Livre'  # Define o status como "Free"

        posts = Post.objects.filter(status=status_param, owner=request.user)

        post_data = []
        for post in posts:
            owner_picture = post.owner.picture
            owner_picture_url = owner_picture.url if owner_picture and owner_picture.name else None
            owner_picture_url_utf8 = owner_picture_url.encode('utf-8').decode('utf-8') if owner_picture_url else None
            post_data.append({
                'id': post.id,
                'created_at': post.created_at,
                'updated_at': post.updated_at,
                'first_name': post.first_name,
                'last_name': post.last_name,
                "nationality": post.nationality,
                "address": post.address,
                "date_of_birth": post.date_of_birth,
                "last_seen_location": post.last_seen_location,
                "cellphone": post.cellphone,
                "cellphone1": post.cellphone1,
                "description": post.description,
                "disease": post.disease,
                "picture": post.picture.url,
                "status": post.status,
                'kinship': post.kinship,
                'province': post.province,
                'gender': post.gender,
                'allergies': post.allergies,
                'owner_picture': owner_picture_url_utf8 if owner_picture_url else None,
                'medical_conditions': post.medical_conditions,
                'medications': post.medications,
                "is_complete": post.is_complete,
                'owner_first_name': post.owner.first_name,
                'owner_last_name': post.owner.last_name,
            })

        return Response(post_data)
    except Post.DoesNotExist:
        return Response({'error': 'No posts found'})
