"""
URL patterns for accounts app - your roadmap to user management 🗺️
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserRegistrationView,
    UserLoginView,
    UserProfileViewSet,
    LogoutView,
    UserFollowView,
)

# Create a router for ViewSets
router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet, basename='profile')

urlpatterns = [
    # Authentication endpoints - the gateway to our app 🚪
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UserProfileViewSet.as_view(), name='profile'),
    path('feed/', FeedView.as_view(), name='feed'),
    
    # Include router URLs
    path('', include(router.urls)),
    path('follow/<int:user_id>/', UserFollowView.as_view(), name='follow'),
    path('unfollow/<int:user_id>/', UserFollowView.as_view(), name='unfollow'),
]