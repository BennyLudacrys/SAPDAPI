# comments/models.py
from django.db import models

from posts.models import Post
from users.models import User


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    author_profile_picture = models.ImageField(upload_to='comment_author_pictures', blank=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comentário de {self.author.username} em {self.post.title}'

    def get_author_profile_picture_url(self):
        if self.author.picture:
            return self.author.picture.url
        # Se não houver uma foto de perfil, você pode retornar uma URL padrão ou None
        return None

