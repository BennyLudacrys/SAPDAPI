import urllib.request

import face_recognition
import numpy as np
import vonage
from PIL import Image, ImageDraw
from cloudinary import uploader
from django.http import JsonResponse
from posts.models import Post
from rest_framework.decorators import api_view


@api_view(['POST'])
def detect_image(request):

    # Upload para cloudinary
    if request.method == 'POST' and request.FILES.get('image'):
        myfile = request.FILES['image']
        response = uploader.upload(myfile)
        uploaded_file_url = response['secure_url']

        # Busca faces e dados da database
        images = []
        encodings = []
        names = []
        files = []
        person_data = []  # Lista de dados das pessoas reconhecidas

        posts = Post.objects.all()
        for post in posts:
            images.append(post.first_name + '_image')
            encodings.append(post.first_name + '_face_encoding')
            files.append(post.picture)
            names.append(post.first_name + ' ' + post.address)

        # Carregar codificações e nomes de rostos conhecidos
        known_face_encodings = []
        for i, image_path in enumerate(files):
            image = face_recognition.load_image_file(image_path)
            encoding = face_recognition.face_encodings(image)
            if len(encoding) > 0:
                known_face_encodings.append(encoding[0])

        known_face_names = names

        # Baixa a imagem desconhecida do Cloudinary
        urllib.request.urlretrieve(uploaded_file_url, 'unknown_image.jpg')

        # Load the unknown image from the local file
        unknown_image = face_recognition.load_image_file('unknown_image.jpg')

        # Find faces and encodings in the unknown image
        face_locations = face_recognition.face_locations(unknown_image)
        face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

        # Check if any faces were detected
        if len(face_encodings) == 0:
            # No faces were detected
            return JsonResponse({'error': 'Nenhuma face detectada na imagem.'})

        # Convert the image to a PIL-format image
        pil_image = Image.fromarray(unknown_image)
        draw = ImageDraw.Draw(pil_image)

        # Loop through each face found in the unknown image
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Desconhecido"
            data = {}  # Dados da pessoa

            # Find the best match
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:

                name = known_face_names[best_match_index]
                post = posts[int(best_match_index)]
                owner_picture = post.owner.picture
                owner_picture_url = owner_picture.url if owner_picture and owner_picture.name else None
                owner_picture_url_utf8 = owner_picture_url.encode('utf-8').decode(
                    'utf-8') if owner_picture_url else None

                data['first_name'] = post.first_name
                data['last_name'] = post.last_name
                data['address'] = post.address
                data['latitude'] = post.latitude
                data['longitude'] = post.longitude
                data['status'] = post.status
                data['cellphone'] = post.cellphone
                data['cellphone1'] = post.cellphone1
                data['description'] = post.description
                data['created_at'] = post.created_at
                data['owner_picture'] = owner_picture_url_utf8
                data['owner_first_name'] = post.owner.first_name
                data['owner_last_name'] = post.owner.last_name
                data['identified_by'] = request.user.username
                data['detected_by_count'] = post.get_detected_by_count()

                # 'updated_at': post.updated_at,
                # "nationality": post.nationality,
                # "address": post.address,
                # "date_of_birth": post.date_of_birth,
                # "last_seen_location": post.last_seen_location,
                # "cellphone": post.cellphone,
                # "cellphone1": post.cellphone1,
                # "description": post.description,
                # "disease": post.disease,
                # "picture": post.picture.url,
                # "status": post.status,
                # "is_complete": post.is_complete,
                # 'kinship': post.kinship,
                # 'province': post.province,
                # 'gender': post.gender,
                # 'allergies': post.allergies,
                # 'medical_conditions': post.medical_conditions,
                # 'medications': post.medications,
                # # 'owner_first_name': post.owner.first_name,
                # # 'owner_last_name': post.owner.last_name,
                # # Adicione outros campos do modelo Post que você deseja retornar
                # 'detected_by_count': detected_by_count,

                # client = vonage.Client(key="5f57e8e9", secret="Y1J1ELPXBgaj3n6T")
                # sms = vonage.Sms(client)
                #
                # message_body = f"Ola, informamos que a(o) senhor(a) : {data['first_name']} {data['last_name']}\n"
                # message_body += f"foi Encontrado e identificado no endereco: {data['address']}\n"
                # message_body += f"pode entrar em contacto pelos numeros: {data['cellphone']}\n"
                # message_body += f"que responde pelo nome de: {data['identified_by']}"
                # message_body += f"Obrigado por usar a nossa aplicacao. Ate breve!"
                # responseData = sms.send_message(
                #     {
                #         "from": "Vonage APIs",
                #         "to": "258860240592",
                #         "text": message_body,
                #     }
                # )
                #
                # if responseData["messages"][0]["status"] == "0":
                #     print("Mensagem enviada com sucesso.")
                # else:
                #     print(f"Falha ao enviar a mensagem. erro: {responseData['messages'][0]['error-text']}")

                # Check if the person is already detected by the current user
                if request.user not in post.detected_by.all():
                    post.detected_by.add(request.user)
                    post.save()

                else:
                    data['error'] = 'Person already detected by this user.'

            # Draw a box around the face
            draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))

            # Draw a label with the name below the face
            text_width, text_height = draw.textsize(name)
            draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
            draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))

            # Append the person's data to the list
            person_data.append(data)
        # Remove the drawing library from memory
        del draw

        # Save the resulting image to Cloudinary
        result_image_path = 'result_image.jpg'
        pil_image.save(result_image_path)
        result_image_response = uploader.upload(result_image_path)
        result_image_url = result_image_response['secure_url']

        # Return the result as a JSON response
        return JsonResponse({'result_image_url': result_image_url, 'person_data': person_data})

    return JsonResponse({'error': 'No image file was provided.'})
