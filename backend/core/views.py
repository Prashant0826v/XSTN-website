from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import JoinCommunity, InternshipApplication, ContactMessage
from .serializers import (
    JoinCommunitySerializer, InternshipApplicationSerializer, ContactMessageSerializer,
    UserSerializer, UserRegistrationSerializer, UserLoginSerializer
)


class JoinCommunityViewSet(viewsets.ModelViewSet):
    queryset = JoinCommunity.objects.all()
    serializer_class = JoinCommunitySerializer


class InternshipApplicationViewSet(viewsets.ModelViewSet):
    queryset = InternshipApplication.objects.all()
    serializer_class = InternshipApplicationSerializer


class ContactMessageViewSet(viewsets.ModelViewSet):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def join_community_api(request):
    """API endpoint for submitting join community form"""
    serializer = JoinCommunitySerializer(data=request.data)
    if serializer.is_valid():
        instance = serializer.save()
        
        # Send confirmation email to user
        try:
            user_email = instance.email
            subject = "Welcome to XSTN Community!"
            message = f"""Thank you for joining XSTN Community!

Dear {instance.full_name},

Thank you for your interest in joining the XSTN community. We appreciate your support and look forward to connecting with you soon.

Your submission details:
- Name: {instance.full_name}
- Email: {instance.email}
- Role: {instance.role}
- Message: {instance.message}

We will review your application and get back to you shortly.

Best regards,
XSTN Team
www.xstn.com
"""
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email], fail_silently=True)
            
            # Send admin notification
            admin_subject = f"New Join Community Submission - {instance.full_name}"
            admin_message = f"""New Join Community submission received!

Name: {instance.full_name}
Email: {instance.email}
Role: {instance.role}
Message: {instance.message}

Please log in to admin panel to review: http://127.0.0.1:8000/admin/
"""
            send_mail(admin_subject, admin_message, settings.DEFAULT_FROM_EMAIL, [settings.ADMIN_EMAIL], fail_silently=True)
        except Exception as e:
            print(f"Error sending email: {str(e)}")
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def internship_application_api(request):
    """API endpoint for submitting internship application form"""
    serializer = InternshipApplicationSerializer(data=request.data)
    if serializer.is_valid():
        instance = serializer.save()
        
        # Send confirmation email to user
        try:
            user_email = instance.email
            subject = "Internship Application Received - XSTN"
            message = f"""Thank you for applying to XSTN Internship Program!

Dear {instance.full_name},

Thank you for your interest in the XSTN Internship Program. We have received your application and appreciate your enthusiasm.

Your submission details:
- Name: {instance.full_name}
- Email: {instance.email}
- Phone: {instance.phone}
- Position Applied: {instance.position}
- Experience: {instance.experience}

We will carefully review your application and contact you within 48 hours with updates.

Best regards,
XSTN Team - Internship Program
www.xstn.com
"""
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email], fail_silently=True)
            
            # Send admin notification
            admin_subject = f"New Internship Application - {instance.full_name}"
            admin_message = f"""New Internship Application received!

Name: {instance.full_name}
Email: {instance.email}
Phone: {instance.phone}
Position: {instance.position}
Experience: {instance.experience}

Please log in to admin panel to review: http://127.0.0.1:8000/admin/
"""
            send_mail(admin_subject, admin_message, settings.DEFAULT_FROM_EMAIL, [settings.ADMIN_EMAIL], fail_silently=True)
        except Exception as e:
            print(f"Error sending email: {str(e)}")
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def contact_message_api(request):
    """API endpoint for submitting contact form"""
    serializer = ContactMessageSerializer(data=request.data)
    if serializer.is_valid():
        instance = serializer.save()
        
        # Send confirmation email to user
        try:
            user_email = instance.email
            subject = "We received your message - XSTN"
            message = f"""We received your message!

Dear {instance.full_name},

Thank you for contacting XSTN. We have received your message and appreciate you reaching out to us.

Your submission details:
- Name: {instance.full_name}
- Email: {instance.email}
- Subject: {instance.subject}
- Message: {instance.message}

Our team will review your inquiry and respond within 24 hours.

Best regards,
XSTN Team - Customer Support
www.xstn.com
"""
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email], fail_silently=True)
            
            # Send admin notification
            admin_subject = f"New Contact Message - {instance.subject}"
            admin_message = f"""New Contact Message received!

Name: {instance.full_name}
Email: {instance.email}
Subject: {instance.subject}
Message: {instance.message}

Please log in to admin panel to review: http://127.0.0.1:8000/admin/
"""
            send_mail(admin_subject, admin_message, settings.DEFAULT_FROM_EMAIL, [settings.ADMIN_EMAIL], fail_silently=True)
        except Exception as e:
            print(f"Error sending email: {str(e)}")
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Authentication Endpoints
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """User registration endpoint"""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            'message': 'User registered successfully',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """User login endpoint - returns JWT tokens"""
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                return Response({
                    'message': 'Login successful',
                    'user': UserSerializer(user).data,
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                }, status=status.HTTP_200_OK)
            else:
                return Response(
                    {'error': 'Invalid credentials'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        except User.DoesNotExist:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    """Get current user profile - requires authentication"""
    return Response({
        'user': UserSerializer(request.user).data
    }, status=status.HTTP_200_OK)
