#Views para ver fotos
from rest_framework import generics, permissions
from .models import Photo
from .serializers import PhotoSerializer
from django.views.generic import ListView
from interactions.models import Follow
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

class PhotoUploadView(generics.CreateAPIView): #endpoint POST
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = [permissions.IsAuthenticated] #requiere JWT

    def perform_create(self, serializer): # Guarda el usuario automaticamente
        serializer.save(user=self.request.user)

#endpoint para ver fotos
class PhotoListView(generics.ListAPIView):
    queryset = Photo.objects.all().order_by("-created_at")
    serializer_class = PhotoSerializer

# Feed Optimizado
class FeedView(LoginRequiredMixin, ListView):

    model = Photo
    template_name = "feed.html"
    context_object_name = "photos"

    def get_queryset(self):

        user = self.request.user

        following_ids = Follow.objects.filter(
            follower=user # Busca a quien sigues 
        ).values_list("following_id", flat=True) # Solo mostrara fotos de gente que sigues 

        return (
            Photo.objects
            .filter(user_id__in=following_ids)
            .select_related("user") #Evita COnsultas extra al usuario
            .prefetch_related("likes", "comments") # Carga todos los likes y comentarios en una sola query extra
            .order_by("-created_at")
        )

class PhotoFeedAPI(ListAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = PhotoSerializer

    def get_queryset(self):

        user = self.request.user

        following_ids = user.following.values_list(
            "following_id",
            flat=True
        )

        return (
            Photo.objects
            .filter(user_id__in=following_ids)
            .select_related("user")
            .prefetch_related("likes", "comments")
            .order_by("-created_at")
        )
