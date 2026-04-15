from rest_framework import serializers
from django.contrib.auth.models import User
from photos.models import Photo
from users.models import Profile
from interactions.models import Message, Conversation, ConversationUser


# --- Fotos del perfil ---
class UserPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ["id", "image", "caption"]


# --- Perfil completo ---
class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    name = serializers.CharField(source="user.first_name")
    photos = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ["username", "name", "avatar", "bio", "photos"]

    def get_photos(self, obj):
        photos = Photo.objects.filter(user=obj.user)
        return UserPhotoSerializer(photos, many=True).data


# --- Usuario simple (chat) ---
class SimpleUserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    name = serializers.CharField(source="first_name")

    class Meta:
        model = User
        fields = ["id", "username", "name", "avatar"]

    def get_avatar(self, obj):
        if hasattr(obj, "profile") and obj.profile.avatar:
            return obj.profile.avatar.url
        return None


# --- Último mensaje ---
class LastMessageSerializer(serializers.ModelSerializer):
    sender = SimpleUserSerializer()

    class Meta:
        model = Message
        fields = ["id", "text", "sender", "created_at"]


# --- Conversación ---
class ConversationSerializer(serializers.ModelSerializer):
    other_user = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ["id", "other_user", "last_message", "unread_count"]

    def get_other_user(self, obj):
        request_user = self.context["request"].user
        other = obj.users.exclude(id=request_user.id).first()

        data = SimpleUserSerializer(other).data
        data["is_online"] = other.profile.is_online if hasattr(other, "profile") else False
        return data

    def get_last_message(self, obj):
        last_msg = obj.messages.order_by("-created_at").first()
        if last_msg:
            return LastMessageSerializer(last_msg).data
        return None

    def get_unread_count(self, obj):
        user = self.context["request"].user
        cu = ConversationUser.objects.filter(conversation=obj, user=user).first()
        if not cu:
            return 0
        return cu.unread_count


# --- Mensajes ---
class MessageSerializer(serializers.ModelSerializer):
    sender = SimpleUserSerializer()

    class Meta:
        model = Message
        fields = ["id", "text", "image", "sender", "created_at"]
