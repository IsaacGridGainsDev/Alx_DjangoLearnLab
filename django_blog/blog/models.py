# blog/models.py
from django.db import models
from django.contrib.auth.models import User
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

class Comment(models.Model):
    """
    Comment model: many-to-one from Comment -> Post, author is a User.
    """
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"

    def get_edit_url(self):
        return reverse("comment-edit", args=[str(self.pk)])

    def get_delete_url(self):
        return reverse("comment-delete", args=[str(self.pk)])