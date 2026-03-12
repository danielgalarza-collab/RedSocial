from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Like, Comment, Follow, Notification


@receiver(post_save, sender=Like)
def create_like_notification(sender, instance, created, **kwargs):

    if created:

        Notification.objects.create(
            recipient=instance.photo.user,
            sender=instance.user,
            notification_type="like",
            photo=instance.photo
        )

@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):

    if created:

        Notification.objects.create(
            recipient=instance.photo.user,
            sender=instance.user,
            notification_type="comment",
            photo=instance.photo
        )

@receiver(post_save, sender=Follow)
def create_follow_notification(sender, instance, created, **kwargs):

    if created:

        Notification.objects.create(
            recipient=instance.following,
            sender=instance.follower,
            notification_type="follow"
        )
