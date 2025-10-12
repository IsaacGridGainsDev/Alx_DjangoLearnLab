"""
Custom User Model - Because regular users are too mainstream 😎
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator

class CustomUser(AbstractUser):
    """
    Extended User model with social media features
    Like Instagram, but we built it ourselves 💪
    """
    
    # Profile fields - making users more interesting since 2024
    bio = models.TextField(
        max_length=500,
        blank=True,
        help_text="Tell the world your story in 500 chars or less"
    )
    
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True,
        help_text="Your beautiful face goes here 📸"
    )
    
    # Followers relationship - it's complicated 💔
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following',
        blank=True,
        help_text="People who think you're awesome"
    )
    
    # Timestamps - because we like to know when things happen
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Additional fields for better UX
    is_verified = models.BooleanField(
        default=False,
        help_text="Blue checkmark dreams ✅"
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"@{self.username}"
    
    def follow(self, user):
        """Follow another user - slide into their followers list"""
        if user != self:  # Can't follow yourself, narcissist!
            user.followers.add(self)
    
    def unfollow(self, user):
        """Unfollow a user - it's not you, it's me"""
        user.followers.remove(self)
    
    def is_following(self, user):
        """Check if following a user"""
        return user.followers.filter(id=self.id).exists()
    
    @property
    def followers_count(self):
        """Count followers - for the ego boost"""
        return self.followers.count()
    
    @property
    def following_count(self):
        """Count following - showing you care"""
        return self.following.count()