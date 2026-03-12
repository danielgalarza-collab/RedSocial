from rest_framework import serializers
from .models import Photo

class PhotoSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(
        source="likes.count",
        read_only=True
    )

    comments_count = serializers.IntegerField(
        source="comments.count",
        read_only=True
    )

    class Meta:
        model = Photo
        fields = [
            "id",
            "user",
            "image",
            "caption",
            "created_at",
            "likes_count",
            "comments_count",
        ]
        read_only_fields = ["user", "created_at"] # el usuario no puede mandar esos datos , el backend los asigna
