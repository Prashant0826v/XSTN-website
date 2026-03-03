from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str, force_bytes

from .models import User
from .serializers import (
    UserSerializer, UserCreateSerializer, EmailVerificationSerializer,
    ResendVerificationSerializer, PasswordResetRequestSerializer,
    PasswordResetSerializer, PasswordChangeSerializer
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for User management with enhanced security"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == 'register':
            return UserCreateSerializer
        elif self.action == 'verify_email':
            return EmailVerificationSerializer
        elif self.action == 'resend_verification':
            return ResendVerificationSerializer
        elif self.action == 'request_password_reset':
            return PasswordResetRequestSerializer
        elif self.action == 'reset_password':
            return PasswordResetSerializer
        elif self.action == 'change_password':
            return PasswordChangeSerializer
        return UserSerializer

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        """
        Register new user with email verification
        POST /api/users/register/
        """
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            self._send_verification_email(user)
            self._send_admin_registration_notification(user)
            return Response({
                'message': 'Registration successful. Please verify your email.',
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def verify_email(self, request):
        """
        Verify email with verification code
        POST /api/users/verify-email/
        """
        serializer = EmailVerificationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            code = serializer.validated_data.get('code')

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response(
                    {'detail': 'User not found.'},
                    status=status.HTTP_404_NOT_FOUND
                )

            if user.is_verified:
                return Response(
                    {'detail': 'Email already verified.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not user.is_verification_code_valid(code):
                return Response(
                    {'detail': 'Invalid or expired verification code.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user.verify_email()
            return Response({
                'message': 'Email verified successfully. You can now log in.',
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def resend_verification(self, request):
        """
        Resend verification email
        POST /api/users/resend-verification/
        """
        serializer = ResendVerificationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                # Don't reveal if email exists or not for security
                return Response(
                    {'message': 'If email exists, verification code has been sent.'},
                    status=status.HTTP_200_OK
                )

            if user.is_verified:
                return Response(
                    {'detail': 'Email already verified.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user.generate_verification_code()
            user.save()
            self._send_verification_email(user)

            return Response(
                {'message': 'Verification code has been sent to your email.'},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """
        Get current authenticated user
        GET /api/users/me/
        """
        user = request.user
        user.last_activity = timezone.now()
        user.save(update_fields=['last_activity'])
        serializer = UserSerializer(user)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        """
        Change password for authenticated user
        POST /api/users/change-password/
        """
        user = request.user
        serializer = PasswordChangeSerializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.validated_data.get('old_password')
            new_password = serializer.validated_data.get('new_password')

            if not user.check_password(old_password):
                return Response(
                    {'detail': 'Old password is incorrect.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user.set_password(new_password)
            user.save()

            return Response(
                {'message': 'Password changed successfully.'},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def request_password_reset(self, request):
        """
        Request password reset email
        POST /api/users/request-password-reset/
        """
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')

            try:
                user = User.objects.get(email=email)
                token = user.generate_password_reset_token()
                user.save()
                self._send_password_reset_email(user, token)
            except User.DoesNotExist:
                pass  # Don't reveal if email exists

            return Response(
                {'message': 'If email exists, password reset link has been sent.'},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def reset_password(self, request):
        """
        Reset password with token
        POST /api/users/reset-password/
        """
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data.get('token')
            password = serializer.validated_data.get('password')

            try:
                user = User.objects.get(password_reset_token=token)
            except User.DoesNotExist:
                return Response(
                    {'detail': 'Invalid password reset token.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not user.is_password_reset_token_valid(token):
                return Response(
                    {'detail': 'Password reset token has expired.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user.set_password(password)
            user.password_reset_token = None
            user.password_reset_expires = None
            user.save()

            return Response(
                {'message': 'Password reset successfully. You can now log in.'},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _send_verification_email(self, user):
        """Send verification email to user"""
        subject = "Verify your XSTN Account"
        message = f"""
Hello {user.first_name or 'User'},

Welcome to XSTN! To complete your registration, please verify your email address using the code below.

Your Verification Code: {user.email_verification_code}

This code will expire in 4 minutes.

If you didn't create this account, please ignore this email.

Best regards,
XSTN Team
https://xstn.tech
        """
        
        html_message = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f5f5; }}
        .container {{ max-width: 600px; margin: 20px auto; padding: 20px; background: white; border-radius: 10px; }}
        .header {{ color: #00d4ff; font-size: 24px; margin-bottom: 20px; }}
        .code {{ background: #f0f0f0; padding: 15px; border-radius: 5px; text-align: center; font-size: 32px; font-weight: bold; color: #00d4ff; margin: 20px 0; letter-spacing: 5px; }}
        .footer {{ color: #666; font-size: 12px; margin-top: 20px; border-top: 1px solid #eee; padding-top: 10px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">Welcome to XSTN!</div>
        <p>Hello {user.first_name or 'User'},</p>
        <p>Thank you for registering. To complete your signup, please verify your email address.</p>
        <div class="code">{user.email_verification_code}</div>
        <p>Enter this code on the verification page or in the app. This code will expire in 4 minutes.</p>
        <p>If you didn't create this account, please ignore this email.</p>
        <div class="footer">
            <p>XSTN Team | https://xstn.tech</p>
        </div>
    </div>
</body>
</html>
        """
        
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                html_message=html_message,
                fail_silently=False
            )
        except Exception as e:
            print(f"Error sending verification email: {str(e)}")

    def _send_password_reset_email(self, user, token):
        """Send password reset email to user"""
        reset_link = f"https://xstn.tech/reset-password?token={token}"
        
        subject = "Reset Your XSTN Password"
        message = f"""
Hello {user.first_name or 'User'},

We received a request to reset your password. Click the link below to proceed.

{reset_link}

This link will expire in 1 hour. If you didn't request this, please ignore this email.

Best regards,
XSTN Team
https://xstn.tech
        """

        html_message = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f5f5; }}
        .container {{ max-width: 600px; margin: 20px auto; padding: 20px; background: white; border-radius: 10px; }}
        .header {{ color: #00d4ff; font-size: 24px; margin-bottom: 20px; }}
        .button {{ display: inline-block; background: #00d4ff; color: #000; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
        .footer {{ color: #666; font-size: 12px; margin-top: 20px; border-top: 1px solid #eee; padding-top: 10px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">Password Reset Request</div>
        <p>Hello {user.first_name or 'User'},</p>
        <p>We received a request to reset your password. Click the button below to proceed.</p>
        <a href="{reset_link}" class="button">Reset Password</a>
        <p>This link will expire in 1 hour.</p>
        <p>If you didn't request this, please ignore this email and your password will remain unchanged.</p>
        <div class="footer">
            <p>XSTN Team | https://xstn.tech</p>
        </div>
    </div>
</body>
</html>
        """

        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                html_message=html_message,
                fail_silently=False
            )
        except Exception as e:
            print(f"Error sending password reset email: {str(e)}")

    def _send_admin_registration_notification(self, user):
        """Send admin notification email for new user registration"""
        admin_email = settings.DEFAULT_FROM_EMAIL
        
        subject = "🎉 New User Registration - XSTN"
        message = f"""
New User Registration Received!

User Details:
- Name: {user.first_name} {user.last_name}
- Email: {user.email}
- Username: {user.username}
- Registration Time: {user.created_at.strftime('%Y-%m-%d %H:%M:%S')}

The user will receive a verification code and must verify their email before they can log in.

Best regards,
XSTN System
        """
        
        html_message = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f5f5; }}
        .container {{ max-width: 600px; margin: 20px auto; padding: 20px; background: white; border-radius: 10px; }}
        .header {{ color: #00d4ff; font-size: 24px; margin-bottom: 20px; text-align: center; }}
        .emoji {{ font-size: 32px; margin-right: 10px; }}
        .user-info {{ background: #f0f0f0; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        .info-row {{ margin: 10px 0; padding: 8px; border-left: 3px solid #00d4ff; padding-left: 12px; }}
        .label {{ font-weight: bold; color: #333; }}
        .value {{ color: #666; }}
        .footer {{ color: #666; font-size: 12px; margin-top: 20px; border-top: 1px solid #eee; padding-top: 10px; text-align: center; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header"><span class="emoji">🎉</span>New User Registration</div>
        <p>A new user has registered for XSTN!</p>
        
        <div class="user-info">
            <div class="info-row">
                <span class="label">Name:</span> 
                <span class="value">{user.first_name} {user.last_name}</span>
            </div>
            <div class="info-row">
                <span class="label">Email:</span> 
                <span class="value">{user.email}</span>
            </div>
            <div class="info-row">
                <span class="label">Username:</span> 
                <span class="value">{user.username}</span>
            </div>
            <div class="info-row">
                <span class="label">Registration Time:</span> 
                <span class="value">{user.created_at.strftime('%Y-%m-%d %H:%M:%S')}</span>
            </div>
        </div>
        
        <p><strong>Status:</strong> Verification email sent to user. Awaiting email verification.</p>
        
        <div class="footer">
            <p>XSTN Admin Notification System</p>
        </div>
    </div>
</body>
</html>
        """
        
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[admin_email],
                html_message=html_message,
                fail_silently=False
            )
        except Exception as e:
            print(f"Error sending admin registration notification: {str(e)}")

