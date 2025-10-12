"""
Filters for posts app - finding needles in the haystack 🔍
"""

from django_filters import rest_framework as filters
from .models import Post, Comment

class PostFilter(filters.FilterSet):
    """
    Post filter - because scrolling endlessly is so 2010 📜
    """
    title = filters.CharFilter(lookup_expr='icontains')
    content = filters.CharFilter(lookup_expr='icontains')
    author = filters.CharFilter(field_name='author__username', lookup_expr='icontains')
    created_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'author', 'is_published']


class CommentFilter(filters.FilterSet):
    """
    Comment filter - finding the gems in the discussion 💎
    """
    author = filters.CharFilter(field_name='author__username', lookup_expr='icontains')
    content = filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = Comment
        fields = ['post', 'author', 'content', 'is_active']