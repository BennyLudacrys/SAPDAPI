from rest_framework import serializers

from comments.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    author_profile_picture = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'text', 'created_at', 'author_name', 'author_profile_picture']

    def get_author_name(self, obj):
        return obj.author.username if obj.author else "Anonymous"

    def get_author_profile_picture(self, obj):
        return obj.get_author_profile_picture_url() if obj.author else None

