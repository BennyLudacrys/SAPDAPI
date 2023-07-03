import cloudinary
from rest_framework.decorators import api_view
from cloudinary_storage.storage import RawMediaCloudinaryStorage
from django.conf import settings
from rest_framework.response import Response
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw
import face_recognition
import numpy as np
from posts.models import Post


@api_view(['POST'])
def detect_image(request):
    if 'image' not in request.FILES:
        return Response({'error': 'Nenhuma imagem fornecida.'}, status=400)

    # Upload image
    storage = RawMediaCloudinaryStorage()
    images = []
    encodings = []
    names = []
    files = []

    posts = Post.objects.all()
    for post in posts:
        images.append(post.first_name + '_image')
        encodings.append(post.first_name + '_face_encoding')
        files.append(post.picture.name)
        names.append(post.first_name + ' ' + post.address)

    for i in range(0, len(images)):
        file_obj = storage.open(files[i])
        images[i] = face_recognition.load_image_file(file_obj)
        encodings[i] = face_recognition.face_encodings(images[i])[0]

    known_face_encodings = encodings
    known_face_names = names

    image = request.FILES['image']
    uploaded_file_name = default_storage.save(image.name, ContentFile(image.read()))
    uploaded_file_url = default_storage.url(uploaded_file_name)

    unknown_image = face_recognition.load_image_file(uploaded_file_url[1:])
    face_locations = face_recognition.face_locations(unknown_image)
    face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

    pil_image = Image.fromarray(unknown_image)
    draw = ImageDraw.Draw(pil_image)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Desconhecido"

        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))
        text_width, text_height = draw.textsize(name)
        draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
        draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))

    del draw

    # Salvar a imagem resultante
    result_image_name = f"image_with_boxes_{uploaded_file_name}"
    result_image_path = f"media/{result_image_name}"
    pil_image.save(result_image_path)

    return Response({'result_image': result_image_name})
