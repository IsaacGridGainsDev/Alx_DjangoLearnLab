from django.shortcuts import render

# Create your views here.
"""
Views for the accounts app - where the magic happens ✨
"""

from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from .models import CustomUser
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    FollowSerializer
)

class UserRegistrationView(generics.CreateAPIView):
    """
    Register new users - welcome to our social network! 🎉
    """
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        """Create user and return with token"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        return Response(
            {
                'message': 'User created successfully! Welcome aboard! 🚀',
                'user': UserProfileSerializer(user).data,
                'token': user.token
            },
            status=status.HTTP_201_CREATED
        )


class UserLoginView(generics.CreateAPIView):
    """
    Login users - your session starts here! 🔐
    """
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        """Authenticate and return token"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        
        return Response(
            {
                'message': 'Login successful! Welcome back! 👋',
                'token': data['token'],
                'user': serializer.get_user(data)
            },
            status=status.HTTP_200_OK
        )


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for user profiles - CRUD operations with style 😎
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter queryset based on user permissions"""
        queryset = super().get_queryset()
        # Optionally filter by username
        username = self.request.query_params.get('username', None)
        if username:
            queryset = queryset.filter(username__icontains=username)
        return queryset
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user's profile - it's all about me! 🤳"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['patch'])
    def update_profile(self, request):
        """Update current user's profile - glow up time! ✨"""
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(
            {
                'message': 'Profile updated successfully! Looking good! 😎',
                'user': serializer.data
            }
        )
    
    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None):
        """Follow a user - joining their fan club! 👥"""
        user_to_follow = self.get_object()
        
        if request.user == user_to_follow:
            return Response(
                {'error': "You can't follow yourself! Nice try though 😄"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        request.user.follow(user_to_follow)
        
        return Response(
            {
                'message': f'You are now following @{user_to_follow.username}! 🎉',
                'following': True
            }
        )
    
    @action(detail=True, methods=['post'])
    def unfollow(self, request, pk=None):
        """Unfollow a user - parting ways 👋"""
        user_to_unfollow = self.get_object()
        
        if request.user == user_to_unfollow:
            return Response(
                {'error': "You can't unfollow yourself! That's deep... 🤔"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        request.user.unfollow(user_to_unfollow)
        
        return Response(
            {
                'message': f'You have unfollowed @{user_to_unfollow.username}',
                'following': False
            }
        )
    
    @action(detail=False, methods=['get'])
    def followers(self, request):
        """Get current user's followers - your fan club! 🌟"""
        followers = request.user.followers.all()
        serializer = UserProfileSerializer(followers, many=True, context={'request': request})
        return Response({
            'count': followers.count(),
            'followers': serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def following(self, request):
        """Get users current user is following - your inspirations! 💫"""
        following = request.user.following.all()
        serializer = UserProfileSerializer(following, many=True, context={'request': request})
        return Response({
            'count': following.count(),
            'following': serializer.data
        })


class LogoutView(APIView):
    """
    Logout view - see you later! 👋
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Delete user's token"""
        try:
            request.user.auth_token.delete()
            return Response(
                {'message': 'Logout successful! Come back soon! 🌈'},
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {'error': 'Something went wrong during logout'},
                status=status.HTTP_400_BAD_REQUEST
            )

#user follow and unfollow class logic
class UserFollowView(APIView):
    """
    Follow and unfollow users - connect with others! 👥
    """
    permission_classes = [IsAuthenticated]
    
    def follow(self, request, pk=None):
        """Follow a user - join their fan club! 👥"""
        user_to_follow = get_object_or_404(CustomUser, id=pk)
        request.user.follow(user_to_follow)
        return Response(
            {'message': f'You are now following @{user_to_follow.username}! 🎉'},
            status=status.HTTP_200_OK
        )
    
    def unfollow(self, request, pk=None):
        """Unfollow a user - parting ways 👋"""
        user_to_unfollow = get_object_or_404(CustomUser, id=pk)
        request.user.unfollow(user_to_unfollow)
        return Response(
            {'message': f'You have unfollowed @{user_to_unfollow.username}'},
            status=status.HTTP_200_OK
        )
