# utils.py or services.py
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import Notification

def create_notification(recipient, actor, verb, target_post=None, target_comment=None):
    """
    Create a notification safely.
    Prevents self-notifications and ensures data integrity.
    """
    if recipient == actor:
        return None  # Don't notify users about their own actions
    Notification.objects.create(
        recipient=recipient,
        actor=actor,
        verb=verb,
        target_post=target_post,
        target_comment=target_comment
    )