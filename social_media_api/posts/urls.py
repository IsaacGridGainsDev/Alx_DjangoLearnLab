"""
URL patterns for posts app - content routing central 🚦
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, FeedView

# Create router
router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    # Feed endpoint - your daily dose of content 📰
    path('feed/', FeedView.as_view(), name='feed'),
    
    # Include router URLs
    path('', include(router.urls)),
    path('feed/', FeedView.as_view(), name='feed'),
    path('<int:pk>/like/', PostLikeView.as_view(), name='like-post'),
    path('<int:pk>/unlike/', PostUnlikeView.as_view(), name='unlike-post'),
]