from django.db import models
from django.contrib.auth.models import User
from photos.models import Photo


class Like(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="likes"
    )

    photo = models.ForeignKey(
        Photo,
        on_delete=models.CASCADE,
        related_name="likes"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "photo")

    def __str__(self):
        return f"{self.user.username} likes {self.photo.id}"


class Comment(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    photo = models.ForeignKey(
        Photo,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} comment on {self.photo.id}"


class Follow(models.Model):

    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following"
    )

    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="followers"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("follower", "following")

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"


#  CHAT

class Conversation(models.Model):
    users = models.ManyToManyField(
        User,
        through="ConversationUser",
        related_name="conversations"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id}"


class ConversationUser(models.Model):
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="participants"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="conversation_data"
    )
    unread_count = models.IntegerField(default=0)

    class Meta:
        unique_together = ("conversation", "user")

    def __str__(self):
        return f"{self.user.username} in conversation {self.conversation.id}"


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE)

    # Texto opcional
    text = models.TextField(null=True, blank=True)

    # Imagen opcional
    image = models.ImageField(upload_to="chat_images/", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    # ✓✓ VISTO
    is_read = models.BooleanField(default=False)

    def __str__(self):
        if self.text:
            return f"{self.sender.username}: {self.text[:20]}"
        return f"{self.sender.username}: [image]"


#  NOTIFICACIONES

class Notification(models.Model):

    NOTIFICATION_TYPES = (
        ("like", "Like"),
        ("comment", "Comment"),
        ("follow", "Follow"),
        ("message", "Message"),
    )

    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_notifications"
    )

    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES
    )

    photo = models.ForeignKey(
        Photo,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender} -> {self.recipient} ({self.notification_type})"
