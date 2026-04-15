from django.urls import path
from .views import (
    ConversationView,
    FollowView,
    LikeAPI,
    CommentAPI,
    ConversationListAPI,
    UserProfileAPI,
    CreateOrGetConversationAPI,
    MessageListAPI,
    SendMessageAPI,
    SendImageAPI,
    mark_as_read,
    NotificationListAPI,
    MarkNotificationsReadAPI,
    mark_as_read
)

urlpatterns = [
    path("conversation/<int:pk>/", ConversationView.as_view(), name="conversation"),
    path("follow/<int:user_id>/", FollowView.as_view(), name="follow"),
    path("like/<int:photo_id>/", LikeAPI.as_view()),
    path("comments/<int:photo_id>/", CommentAPI.as_view()),
    path("chat/conversations/", ConversationListAPI.as_view()),
    path("users/<int:user_id>/profile/", UserProfileAPI.as_view()),
    path("chat/start/", CreateOrGetConversationAPI.as_view()),
    path("chat/<int:conversation_id>/messages/", MessageListAPI.as_view()),
    path("chat/<int:conversation_id>/send/", SendMessageAPI.as_view()),
    path("chat/<int:conversation_id>/send-image/", SendImageAPI.as_view()),
    path("notifications/", NotificationListAPI.as_view()),
    path("notifications/read/", MarkNotificationsReadAPI.as_view()),
    path("messages/read/<int:conversation_id>/", mark_as_read),
]
