from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/photos/', include('photos.urls')),
    path("api/interactions/", include("interactions.urls"))
]
