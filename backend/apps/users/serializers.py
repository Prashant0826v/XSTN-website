from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
import re

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """User profile serializer"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone', 
                  'company', 'bio', 'is_verified', 'email_verified_at', 'created_at', 'last_activity']
        read_only_fields = ['id', 'created_at', 'last_activity', 'email_verified_at']


class UserCreateSerializer(serializers.ModelSerializer):
    """User registration serializer with enhanced validation"""
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        style={'input_type': 'password'},
        validators=[validate_password]
    )
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password', 'first_name', 'last_name']

    def validate_email(self, value):
        """Validate email uniqueness"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value

    def validate_username(self, value):
        """Validate username uniqueness and format"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        if not re.match(r'^[a-zA-Z0-9_.-]+$', value):
            raise serializers.ValidationError("Username can only contain letters, numbers, dots, hyphens, and underscores.")
        return value

    def validate(self, data):
        """Validate password confirmation"""
        password = data.get('password')
        confirm_password = data.pop('confirm_password', None)
        
        if password != confirm_password:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        
        return data

    def create(self, validated_data):
        """Create user with email verification code"""
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            password=validated_data['password'],
            is_verified=False
        )
        
        # Generate and send verification code
        user.generate_verification_code()
        user.save()
        
        return user


class EmailVerificationSerializer(serializers.Serializer):
    """Email verification serializer"""
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6, min_length=6)

    def validate_code(self, value):
        """Validate code format"""
        if not value.isdigit():
            raise serializers.ValidationError("Verification code must be 6 digits.")
        return value


class ResendVerificationSerializer(serializers.Serializer):
    """Resend verification code serializer"""
    email = serializers.EmailField()


class PasswordResetRequestSerializer(serializers.Serializer):
    """Password reset request serializer"""
    email = serializers.EmailField()


class PasswordResetSerializer(serializers.Serializer):
    """Password reset serializer"""
    token = serializers.CharField(max_length=100)
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        validators=[validate_password]
    )
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        """Validate password confirmation"""
        password = data.get('password')
        confirm_password = data.pop('confirm_password', None)
        
        if password != confirm_password:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        
        return data


class PasswordChangeSerializer(serializers.Serializer):
    """Change password for authenticated users"""
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        validators=[validate_password]
    )
    confirm_new_password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        """Validate new password confirmation"""
        new_password = data.get('new_password')
        confirm_new_password = data.pop('confirm_new_password', None)
        
        if new_password != confirm_new_password:
            raise serializers.ValidationError({"new_password": "Passwords do not match."})
        
        return data

