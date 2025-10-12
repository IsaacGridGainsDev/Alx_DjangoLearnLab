"""
Models for posts app - where content is king 👑
"""

from django.db import models
from django.conf import settings
from django.utils import timezone

class Post(models.Model):
    """
    Post model - sharing thoughts, one post at a time 📝
    """
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
        help_text="The creative genius behind this post"
    )
    
    title = models.CharField(
        max_length=200,
        help_text="Catchy title to grab attention 🎯"
    )
    
    content = models.TextField(
        help_text="Your thoughts, dreams, and memes go here"
    )
    
    # Media support - because a picture is worth a thousand words 📸
    image = models.ImageField(
        upload_to='posts/',
        blank=True,
        null=True,
        help_text="Optional image to make your post pop!"
    )
    
    # Timestamps - keeping track of time like a boss ⏰
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Engagement metrics
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='liked_posts',
        blank=True,
        help_text="Users who appreciate your content"
    )
    
    # Post visibility
    is_published = models.BooleanField(
        default=True,
        help_text="Toggle to hide/show post"
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['author', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.title} by @{self.author.username}"
    
    @property
    def likes_count(self):
        """Count the love ❤️"""
        return self.likes.count()
    
    @property
    def comments_count(self):
        """Count the conversations 💬"""
        return self.comments.filter(is_active=True).count()
    
    def is_liked_by(self, user):
        """Check if user has liked this post"""
        return self.likes.filter(id=user.id).exists() if user.is_authenticated else False


class Comment(models.Model):
    """
    Comment model - where discussions happen 💬
    """
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        help_text="The post this comment belongs to"
    )
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        help_text="The witty commenter"
    )
    
    content = models.TextField(
        help_text="Share your thoughts, be nice! 😊"
    )
    
    # Parent comment for nested replies
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies',
        help_text="For threaded conversations"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Soft delete support
    is_active = models.BooleanField(
        default=True,
        help_text="False = soft deleted"
    )
    
    class Meta:
        ordering = ['created_at']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
    
    def __str__(self):
        return f"Comment by @{self.author.username} on {self.post.title[:20]}"
    
    @property
    def replies_count(self):
        """Count nested replies"""
        return self.replies.filter(is_active=True).count()


class Like(models.Model):
    """
    Like model - spreading the love ❤️
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='post_likes'
    )
    
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='post_likes_through'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'post']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"@{self.user.username} likes {self.post.title[:20]}"