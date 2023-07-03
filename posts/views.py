import cloudinary
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import PersonSerializer
from cloudinary.uploader import upload as cloudinary_upload
from rest_framework.permissions import IsAuthenticated
from .models import Post


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
        return Post.objects.filter(owner=self.request.user)


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
