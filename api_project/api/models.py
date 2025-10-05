# blog/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    """
    User Profile model (one-to-one with Django's User).
    Stores optional fields such as profile photo and bio.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True)
    profile_photo = models.ImageField(upload_to="profile_photos/", blank=True, null=True)

    def __str__(self):
        return f"Profile for {self.user.username}"


# Signals to auto-create / save Profile whenever User is created or saved
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        # Ensure profile exists and is saved
        instance.profile.save()

from django.urls import reverse

class Post(models.Model):
    """
    Post model - stores blog post content.
    Fields:
      - title: short title
      - content: full body
      - published_date: auto set when created
      - author: FK to User
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

    class Meta:
        ordering = ["-published_date"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # used by CreateView/UpdateView to redirect to detail
        return reverse("post-detail", args=[str(self.pk)])