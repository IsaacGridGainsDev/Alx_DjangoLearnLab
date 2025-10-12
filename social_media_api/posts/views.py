"""
Views for posts app - where content meets API 🚀
"""

from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q, Count
from .models import Post, Comment, Like
from .serializers import (
    PostSerializer,
    PostCreateUpdateSerializer,
    CommentSerializer,
    FeedSerializer
)
from .permissions import IsAuthorOrReadOnly
from .filters import PostFilter, CommentFilter

class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for posts - full CRUD with bells and whistles 🔔
    """
    #Post.objects.all()
    queryset = Post.objects.filter(is_published=True).select_related('author')
    permission_classes = [IsAuthenticated]
    filter_class = PostFilter
    search_fields = ['title', 'content', 'author__username']
    ordering_fields = ['created_at', 'likes_count', 'comments_count']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Choose serializer based on action"""
        if self.action in ['create', 'update', 'partial_update']:
            return PostCreateUpdateSerializer
        return PostSerializer
    
    def get_permissions(self):
        """Custom permissions per action"""
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAuthorOrReadOnly()]
        elif self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        """Optimize queryset with select_related and prefetch_related"""
        queryset = super().get_queryset()
        return queryset.annotate(
            likes_count_anno=Count('likes'),
            comments_count_anno=Count('comments')
        )
    
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """Like a post - spread the love ❤️"""
        post = self.get_object()
        
        if post.likes.filter(id=request.user.id).exists():
            return Response(
                {'message': 'You already liked this post! One like per person 😊'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        post.likes.add(request.user)
        Like.objects.create(user=request.user, post=post)
        
        return Response(
            {
                'message': 'Post liked! Thanks for the love! ❤️',
                'likes_count': post.likes_count
            }
        )
    
    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        """Unlike a post - breaking hearts 💔"""
        post = self.get_object()
        
        if not post.likes.filter(id=request.user.id).exists():
            return Response(
                {'message': "You haven't liked this post yet!"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        post.likes.remove(request.user)
        Like.objects.filter(user=request.user, post=post).delete()
        
        return Response(
            {
                'message': 'Post unliked!',
                'likes_count': post.likes_count
            }
        )
    
    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        """Get all comments for a post - join the conversation! 💬"""
        post = self.get_object()
        comments = post.comments.filter(is_active=True, parent=None)
        
        # Apply pagination
        page = self.paginate_queryset(comments)
        if page is not None:
            serializer = CommentSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def my_posts(self, request):
        """Get current user's posts - your content collection 📚"""
        posts = self.get_queryset().filter(author=request.user)
        
        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for comments - where discussions thrive 💭
    """
    #Comment.objects.all()
    queryset = Comment.objects.filter(is_active=True).select_related('author', 'post')
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    filter_class = CommentFilter
    
    def get_permissions(self):
        """Custom permissions per action"""
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAuthorOrReadOnly()]
        return [IsAuthenticated()]
    
    def perform_destroy(self, instance):
        """Soft delete instead of hard delete - keeping history 📜"""
        instance.is_active = False
        instance.save()
    
    @action(detail=True, methods=['post'])
    def reply(self, request, pk=None):
        """Reply to a comment - keeping the conversation going 🗣️"""
        parent_comment = self.get_object()
        
        serializer = CommentSerializer(
            data={
                'content': request.data.get('content'),
                'post': parent_comment.post.id,
                'parent': parent_comment.id
            },
            context={'request': request}
        )
        
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(
            {
                'message': 'Reply added successfully! 💬',
                'comment': serializer.data
            },
            status=status.HTTP_201_CREATED
        )


class FeedView(generics.ListAPIView):
    """
    Feed view - your personalized content stream 📱
    """
    serializer_class = FeedSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Get posts from users the current user follows"""
        user = self.request.user
        following_users = user.following.all()
        
        # Include user's own posts and posts from following
        queryset = Post.objects.filter(
            Q(author__in=following_users) | Q(author=user),
            is_published=True
        ).select_related('author').prefetch_related('likes', 'comments')
        
        return queryset.order_by('-created_at')