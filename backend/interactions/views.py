from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.db.models import F

from .profile_serializer import (
    ProfileSerializer,
    ConversationSerializer,
    MessageSerializer
)

from .models import (
    Conversation,
    ConversationUser,
    Follow,
    Like,
    Comment,
    Message,
    Notification
)

from backend.photos.models import Photo



#   ESTADO DE UNA CONVERSACIÓN


class ConversationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, conversation_id):
        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return Response({"error": "Conversación no existe"}, status=404)

        if request.user not in conversation.users.all():
            return Response({"error": "No tienes acceso"}, status=403)

        serializer = ConversationSerializer(conversation, context={"request": request})
        return Response(serializer.data)



#   FOLLOW SYSTEM

class FollowView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        follower = request.user
        following = User.objects.get(id=user_id)

        if follower.id == following.id:
            return Response({"detail": "No puedes seguirte a ti mismo."}, status=400)

        follow, created = Follow.objects.get_or_create(
            follower=follower,
            following=following
        )

        if created:
            return Response({"detail": f"Ahora sigues a {following.username}"})
        else:
            return Response({"detail": f"Ya sigues a {following.username}"})


#   LIKE SYSTEM


class LikeAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, photo_id):
        user = request.user

        try:
            photo = Photo.objects.get(id=photo_id)
        except Photo.DoesNotExist:
            return Response({"error": "Photo not found"}, status=404)

        like = Like.objects.filter(user=user, photo=photo).first()

        if like:
            like.delete()
            return Response({"liked": False})
        else:
            Like.objects.create(user=user, photo=photo)
            return Response({"liked": True})



#   COMMENTS


class CommentAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, photo_id):
        comments = Comment.objects.filter(photo_id=photo_id).order_by("-created_at")

        data = [
            {
                "id": c.id,
                "user": c.user.username,
                "text": c.text,
                "created_at": c.created_at
            }
            for c in comments
        ]

        return Response(data)

    def post(self, request, photo_id):
        user = request.user
        text = request.data.get("text")

        if not text:
            return Response({"error": "Text required"}, status=400)

        comment = Comment.objects.create(
            user=user,
            photo_id=photo_id,
            text=text
        )

        return Response({
            "id": comment.id,
            "user": user.username,
            "text": comment.text
        })



#   LISTA DE CONVERSACIONES


class ConversationListAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        conversations = request.user.conversations.all()
        serializer = ConversationSerializer(
            conversations,
            many=True,
            context={"request": request}
        )
        return Response(serializer.data)



#   PERFIL DE USUARIO


class UserProfileAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        profile = user.profile
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)



#   CREAR / OBTENER CONVERSACIÓN

class CreateOrGetConversationAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        other_user_id = request.data.get("user_id")

        if not other_user_id:
            return Response({"error": "user_id requerido"}, status=400)

        try:
            other_user = User.objects.get(id=other_user_id)
        except User.DoesNotExist:
            return Response({"error": "Usuario no existe"}, status=404)

        conversation = Conversation.objects.filter(
            users=request.user
        ).filter(
            users=other_user
        ).first()

        if not conversation:
            conversation = Conversation.objects.create()
            conversation.users.add(request.user, other_user)

            ConversationUser.objects.get_or_create(conversation=conversation, user=request.user)
            ConversationUser.objects.get_or_create(conversation=conversation, user=other_user)

        return Response({"conversation_id": conversation.id})



#   LISTA DE MENSAJES


class MessageListAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, conversation_id):
        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return Response({"error": "Conversación no existe"}, status=404)

        if request.user not in conversation.users.all():
            return Response({"error": "No tienes acceso a esta conversación"}, status=403)

        messages = conversation.messages.order_by("created_at")
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)



#   ENVIAR MENSAJE


class SendMessageAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, conversation_id):
        text = request.data.get("text")

        if not text:
            return Response({"error": "Mensaje vacío"}, status=400)

        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return Response({"error": "Conversación no existe"}, status=404)

        if request.user not in conversation.users.all():
            return Response({"error": "No tienes acceso a esta conversación"}, status=403)

        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            text=text
        )

        # Crear notificación
        for other in conversation.users.exclude(id=request.user.id):
            Notification.objects.create(
                recipient=other,
                sender=request.user,
                notification_type="message"
            )

        # unread_count
        ConversationUser.objects.filter(
            conversation=conversation
        ).exclude(
            user=request.user
        ).update(
            unread_count=F("unread_count") + 1
        )

        serializer = MessageSerializer(message)
        return Response(serializer.data, status=201)



#   ENVIAR IMAGEN


class SendImageAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, conversation_id):
        image = request.FILES.get("image")

        if not image:
            return Response({"error": "No image provided"}, status=400)

        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return Response({"error": "Conversación no existe"}, status=404)

        if request.user not in conversation.users.all():
            return Response({"error": "No tienes acceso a esta conversación"}, status=403)

        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            image=image
        )

        ConversationUser.objects.filter(
            conversation=conversation
        ).exclude(
            user=request.user
        ).update(
            unread_count=F("unread_count") + 1
        )

        serializer = MessageSerializer(message)
        return Response(serializer.data, status=201)



#   MARCAR MENSAJES COMO LEÍDOS


@api_view(["POST"])
def mark_as_read(request, conversation_id):
    ConversationUser.objects.filter(
        conversation_id=conversation_id,
        user=request.user
    ).update(unread_count=0)

    return Response({"status": "ok"})



#   LISTA DE NOTIFICACIONES


class NotificationListAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = Notification.objects.filter(
            recipient=request.user
        ).order_by("-created_at")

        data = [
            {
                "id": n.id,
                "sender": n.sender.username,
                "type": n.notification_type,
                "photo": n.photo.id if n.photo else None,
                "is_read": n.is_read,
                "created_at": n.created_at
            }
            for n in notifications
        ]

        return Response(data)



#   MARCAR NOTIFICACIONES COMO LEÍDAS


class MarkNotificationsReadAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        Notification.objects.filter(
            recipient=request.user,
            is_read=False
        ).update(is_read=True)

        return Response({"status": "ok"})
