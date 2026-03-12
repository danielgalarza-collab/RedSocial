from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

from django.views.generic import DetailView
from .models import Conversation, Follow


class ConversationView(DetailView):

    model = Conversation
    template_name = "conversation.html"
    context_object_name = "conversation"


class FollowView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        follower = request.user
        following = User.objects.get(id=user_id)

        # Evita seguirte a ti mismo
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
