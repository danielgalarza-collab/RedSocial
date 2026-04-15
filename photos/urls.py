#URLS De fotos
from django.urls import path
from .views import PhotoUploadView, PhotoListView, FeedView, PhotoFeedAPI

urlpatterns = [
    # API para subir fotos
    path("upload/", PhotoUploadView.as_view(), name="photo-upload"),

    # Lista de fotos (API)
    path("", PhotoListView.as_view(), name="photo-list"),

    # FEED HTML (usa templates)
    path("page/feed/", FeedView.as_view(), name="feed-html"),

    # FEED API (JSON)
    path("feed/", PhotoFeedAPI.as_view(), name="feed-api"),
]
