from django.contrib import admin
from .models import Like, Comment, Follow, Conversation, Message, Notification

admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Follow)
admin.site.register(Conversation)
admin.site.register(Message)
admin.site.register(Notification)
