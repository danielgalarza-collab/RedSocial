from django.urls import path
from .views import ConversationView, FollowView

urlpatterns = [
    path("conversation/<int:pk>/", ConversationView.as_view(), name="conversation"),
    path("follow/<int:user_id>/", FollowView.as_view(), name="follow"),
]
