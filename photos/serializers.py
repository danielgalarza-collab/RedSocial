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

    #saber si el usuario ya dio like
    is_liked = serializers.SerializerMethodField()

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
            "is_liked",
        ]
        read_only_fields = ["user", "created_at"] # el usuario no puede mandar esos datos , el backend los asigna


    def get_is_liked(self, obj):
        user = self.context["request"].user
        if user.is_anonymous:
            return False
        return obj.likes.filter(user=user).exists()
