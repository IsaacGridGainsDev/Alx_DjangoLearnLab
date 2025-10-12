"""
URL patterns for accounts app - your roadmap to user management 🗺️
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserRegistrationView,
    UserLoginView,
    UserProfileViewSet,
    LogoutView
)

# Create a router for ViewSets
router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet, basename='profile')

urlpatterns = [
    # Authentication endpoints - the gateway to our app 🚪
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # Include router URLs
    path('', include(router.urls)),
]