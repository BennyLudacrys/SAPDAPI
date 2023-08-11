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
    # Upload image to Cloudinary
    if request.method == 'POST' and request.FILES.get('image'):
        myfile = request.FILES['image']
        response = uploader.upload(myfile)
        uploaded_file_url = response['secure_url']

        # Fetch known face data from database
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

        # Load known face encodings and names
        known_face_encodings = []
        for i, image_path in enumerate(files):
            image = face_recognition.load_image_file(image_path)
            encoding = face_recognition.face_encodings(image)
            if len(encoding) > 0:
                known_face_encodings.append(encoding[0])

        known_face_names = names

        # Download the unknown image from Cloudinary
        urllib.request.urlretrieve(uploaded_file_url, 'unknown_image.jpg')

        # Load the unknown image from the local file
        unknown_image = face_recognition.load_image_file('unknown_image.jpg')

        # Find faces and encodings in the unknown image
        face_locations = face_recognition.face_locations(unknown_image)
        face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

        # Check if any faces were detected
        if len(face_encodings) == 0:
            # No faces were detected
            return JsonResponse({'error': 'No faces were detected in the image.'})

        # Convert the image to a PIL-format image
        pil_image = Image.fromarray(unknown_image)
        draw = ImageDraw.Draw(pil_image)

        # Loop through each face found in the unknown image
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            data = {}  # Dados da pessoa

            # Find the best match
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                post = posts[int(best_match_index)]
                data['first_name'] = post.first_name
                data['last_name'] = post.last_name
                data['address'] = post.address
                data['status'] = post.status
                data['cellphone'] = post.cellphone
                data['cellphone1'] = post.cellphone1
                data['description'] = post.description
                data['identified_by'] = request.user.username

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
