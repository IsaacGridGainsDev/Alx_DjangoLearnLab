"""
Serializers for the accounts app - turning models into JSON since 2024
"""

from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
#from rest_framework.authtoken.models import Token
from .models import CustomUser

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Registration serializer - creating users like a boss 💪
    """
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        help_text="At least 8 characters, please be creative!"
    )
    password_confirm = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)
    #token = serializers.CharField()
    
    class Meta:
        model = CustomUser
        fields = (
            'id', 'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'bio', 'profile_picture', 'token'
        )
        read_only_fields = ('id',)
    
    def validate(self, attrs):
        """Validate passwords match - because typos happen"""
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError({
                'password': "Password fields didn't match. Try again!"
            })
        return attrs
    
    def create(self, validated_data):
        """Create user and generate token - welcome to the club! 🎉"""
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        
        # Create the user
        user = CustomUser.objects.create_user(
            **validated_data,
            password=password
        )
        #get_user_model().objects.create_user()
        
        # Create auth token
        #Token.objects.create()
        token, _ = Token.objects.get_or_create(user=user)
        
        # Attach token to user object for response
        user.token = token.key
        
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Login serializer - your key to the kingdom 🔑
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)
    user = serializers.SerializerMethodField()
    
    def validate(self, attrs):
        """Authenticate user - checking if you're who you say you are"""
        username = attrs.get('username')
        password = attrs.get('password')
        
        # Authenticate the user
        user = authenticate(username=username, password=password)
        
        if not user:
            raise serializers.ValidationError(
                'Invalid credentials. Did you forget your password? 🤔'
            )
        
        if not user.is_active:
            raise serializers.ValidationError(
                'User account is disabled. Contact support!'
            )
        
        attrs['user'] = user
        return attrs
    
    def create(self, validated_data):
        """Get or create token for authenticated user"""
        user = validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        
        return {
            'token': token.key,
            'user': user
        }
    
    def get_user(self, obj):
        """Return user details in login response"""
        if isinstance(obj, dict) and 'user' in obj:
            user = obj['user']
            return {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
        return None


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Profile serializer - showing off your best self 🌟
    """
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()
    is_following = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomUser
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name',
            'bio', 'profile_picture', 'is_verified',
            'followers_count', 'following_count', 'is_following',
            'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'username', 'email', 'is_verified', 'created_at', 'updated_at')
    
    def get_is_following(self, obj):
        """Check if current user follows this user"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user.is_following(obj)
        return False


class FollowSerializer(serializers.Serializer):
    """
    Follow/Unfollow serializer - managing your social circle 👥
    """
    user_id = serializers.IntegerField()
    action = serializers.ChoiceField(choices=['follow', 'unfollow'])
    
    def validate_user_id(self, value):
        """Check if user exists and not trying to follow yourself"""
        try:
            user = CustomUser.objects.get(id=value)
            request_user = self.context['request'].user
            
            if user == request_user:
                raise serializers.ValidationError(
                    "You can't follow yourself. Self-love is good, but this is too much! 😅"
                )
            return value
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("User not found. Ghost following isn't allowed! 👻")