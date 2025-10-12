"""
Serializers for posts app - transforming content into API gold 🏆
"""

from rest_framework import serializers
from .models import Post, Comment, Like
from accounts.serializers import UserProfileSerializer

class CommentSerializer(serializers.ModelSerializer):
    """
    Comment serializer - for the chatty ones 💬
    """
    author = UserProfileSerializer(read_only=True)
    author_id = serializers.IntegerField(write_only=True, required=False)
    replies_count = serializers.ReadOnlyField()
    replies = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = (
            'id', 'post', 'author', 'author_id', 'content',
            'parent', 'replies', 'replies_count',
            'created_at', 'updated_at', 'is_active'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')
    
    def get_replies(self, obj):
        """Get nested replies - conversation trees! 🌳"""
        if obj.parent is None:  # Only get replies for top-level comments
            replies = obj.replies.filter(is_active=True)[:3]  # Limit to 3 for performance
            return CommentSerializer(replies, many=True).data
        return []
    
    def create(self, validated_data):
        """Create comment with current user as author"""
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class PostSerializer(serializers.ModelSerializer):
    """
    Post serializer - making posts API-ready 📮
    """
    author = UserProfileSerializer(read_only=True)
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()
    is_liked = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = (
            'id', 'author', 'title', 'content', 'image',
            'likes_count', 'comments_count', 'is_liked',
            'comments', 'is_published',
            'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'author', 'created_at', 'updated_at')
    
    def get_is_liked(self, obj):
        """Check if current user liked this post"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.is_liked_by(request.user)
        return False
    
    def get_comments(self, obj):
        """Get top-level comments (not replies)"""
        comments = obj.comments.filter(
            is_active=True,
            parent=None
        )[:5]  # Limit to 5 for performance
        return CommentSerializer(comments, many=True).data
    
    def create(self, validated_data):
        """Create post with current user as author"""
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for creating/updating posts - keep it simple! ✏️
    """
    class Meta:
        model = Post
        fields = ('title', 'content', 'image', 'is_published')
    
    def create(self, validated_data):
        """Create with current user as author"""
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class FeedSerializer(serializers.ModelSerializer):
    """
    Feed serializer - your personalized content stream 📱
    """
    author = UserProfileSerializer(read_only=True)
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()
    is_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = (
            'id', 'author', 'title', 'content', 'image',
            'likes_count', 'comments_count', 'is_liked',
            'created_at'
        )
        read_only_fields = fields
    
    def get_is_liked(self, obj):
        """Check if current user liked this post"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.is_liked_by(request.user)
        return False