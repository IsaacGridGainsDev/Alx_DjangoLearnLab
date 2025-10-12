from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from .models import Notification, Like, Post, Comment
from .serializers import NotificationSerializer

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)

class NotificationMarkReadView(generics.UpdateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Notification.objects.all()

    def get_object(self):
        obj = super().get_object()
        if obj.recipient != self.request.user:
            self.permission_denied(self.request)
        return obj

    def perform_update(self, serializer):
        serializer.save(unread=False)

class LikePostView(generics.GenericAPIView):
    """
    Like a post. Creates a Like and sends a notification to the post author.
    If already liked, unlikes the post (toggle behavior).
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        user = request.user

        if post.author == user:
            return Response(
                {"detail": "You cannot like your own post."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Try to create a like
            like = Like.objects.create(user=user, post=post)

            # Create notification for the post author
            Notification.objects.create(
                recipient=post.author,
                actor=user,
                verb="liked your post",
                target=post
            )

            return Response(
                {"message": f"You liked the post by @{post.author.username}!"},
                status=status.HTTP_201_CREATED
            )
        except IntegrityError:
            # Like already exists → unlike it
            Like.objects.filter(user=user, post=post).delete()
            # Optionally delete any existing notification (optional)
            Notification.objects.filter(
                recipient=post.author,
                actor=user,
                verb="liked your post",
                target=post
            ).delete()

            return Response(
                {"message": "Post unliked."},
                status=status.HTTP_200_OK
            )


# Optional: Separate views for like/unlike (if you prefer explicit endpoints)
# But toggle in one endpoint is common and cleaner.

class UnlikePostView(generics.GenericAPIView):
    """
    Explicitly unlike a post (alternative design).
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        deleted, _ = Like.objects.filter(user=request.user, post=post).delete()
        if deleted:
            # Also remove notification
            Notification.objects.filter(
                recipient=post.author,
                actor=request.user,
                verb="liked your post",
                target=post
            ).delete()
            return Response({"message": "Post unliked."}, status=status.HTTP_200_OK)
        return Response({"message": "Post not liked."}, status=status.HTTP_400_BAD_REQUEST)