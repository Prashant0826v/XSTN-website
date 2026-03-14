from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import (
    JoinCommunity, InternshipApplication, ContactMessage, ProposalForm,
    DeveloperApplication, ConsultationRequest, NewsletterSubscription, Testimonial
)
from .serializers import (
    JoinCommunitySerializer, InternshipApplicationSerializer, ContactMessageSerializer,
    ProposalFormSerializer, DeveloperApplicationSerializer, ConsultationRequestSerializer,
    NewsletterSubscriptionSerializer, TestimonialSerializer,
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


@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])
def test_check_api(request):
    """Simple API check"""
    return Response({'status': 'ok', 'working': True})

@api_view(['GET'])
@permission_classes([AllowAny])
def test_email_api(request):
    """Diagnostic endpoint to test SMTP settings"""
    target_email = request.query_params.get('email', settings.ADMIN_EMAIL)
    subject = "XSTN - SMTP Diagnostic Test"
    message = "If you are reading this, your Railway SMTP settings are working perfectly!"
    
    try:
        send_mail(
            subject, 
            message, 
            settings.DEFAULT_FROM_EMAIL, 
            [target_email], 
            fail_silently=False
        )
        return Response({
            'status': 'success',
            'message': f'Test email sent to {target_email}',
            'backend': settings.EMAIL_BACKEND,
            'from': settings.DEFAULT_FROM_EMAIL
        })
    except Exception as e:
        return Response({
            'status': 'error',
            'error_type': str(type(e).__name__),
            'error_message': str(e),
            'backend': settings.EMAIL_BACKEND
        }, status=500)

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def join_community_api(request):
    """API endpoint for submitting join community form"""
    print(f"DEBUG: join_community_api received request: {request.data}")
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


@csrf_exempt
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


@csrf_exempt
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

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def proposal_form_api(request):
    """API endpoint for submitting proposal form"""
    serializer = ProposalFormSerializer(data=request.data)
    if serializer.is_valid():
        instance = serializer.save()
        
        # Send confirmation email to user
        try:
            user_email = instance.email
            subject = "Project Proposal Received - XSTN"
            message = f"""Thank you for your project proposal!

Dear {instance.name},

Thank you for submitting your project proposal to XSTN. We have received your inquiry and appreciate the opportunity to work with you.

Project Details:
- Company: {instance.company or 'Not specified'}
- Project Type: {instance.project_type}
- Budget Range: {instance.budget_range or 'Not specified'}
- Timeline: {instance.timeline or 'Not specified'}
- Message: {instance.message}

Our team will review your proposal and contact you within 24-48 hours with a customized solution.

Best regards,
XSTN Team - Business Development
www.xstn.tech
"""
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email], fail_silently=True)
            
            # Send admin notification
            admin_subject = f"New Project Proposal - {instance.project_type} from {instance.name}"
            admin_message = f"""New Project Proposal received!

Name: {instance.name}
Email: {instance.email}
Company: {instance.company or 'Not specified'}
Project Type: {instance.project_type}
Budget Range: {instance.budget_range or 'Not specified'}
Timeline: {instance.timeline or 'Not specified'}
Message: {instance.message}

Please log in to admin panel to review: http://localhost:8000/admin/core/proposalform/
"""
            send_mail(admin_subject, admin_message, settings.DEFAULT_FROM_EMAIL, [settings.ADMIN_EMAIL], fail_silently=True)
        except Exception as e:
            print(f"Error sending email: {str(e)}")
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def developer_application_api(request):
    """API endpoint for submitting developer application"""
    serializer = DeveloperApplicationSerializer(data=request.data)
    if serializer.is_valid():
        instance = serializer.save()
        
        # Send confirmation email to user
        try:
            user_email = instance.email
            subject = "Developer Application Received - XSTN"
            message = f"""Thank you for your developer application!

Dear {instance.full_name},

Thank you for your interest in joining XSTN as a developer. We have received your application and appreciate your enthusiasm.

Application Details:
- Name: {instance.full_name}
- Email: {instance.email}
- Phone: {instance.phone}
- Role Interested: {instance.role_interested}
- Experience Level: {instance.experience_level.title()}
- Skills: {instance.skills}
- Message: {instance.message}

We will review your application carefully and contact you within 3-5 business days with updates.

Best regards,
XSTN Team - Recruitment
www.xstn.tech
"""
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email], fail_silently=True)
            
            # Send admin notification
            admin_subject = f"New Developer Application - {instance.role_interested} from {instance.full_name}"
            admin_message = f"""New Developer Application received!

Name: {instance.full_name}
Email: {instance.email}
Phone: {instance.phone}
Role Interested: {instance.role_interested}
Experience Level: {instance.experience_level.title()}
Skills: {instance.skills}
Portfolio URL: {instance.portfolio_url or 'Not provided'}
GitHub URL: {instance.github_url or 'Not provided'}
Message: {instance.message}
Status: {instance.status.title()}

Please log in to admin panel to review: http://localhost:8000/admin/core/developerapplication/
"""
            send_mail(admin_subject, admin_message, settings.DEFAULT_FROM_EMAIL, [settings.ADMIN_EMAIL], fail_silently=True)
        except Exception as e:
            print(f"Error sending email: {str(e)}")
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def consultation_request_api(request):
    """API endpoint for submitting consultation request"""
    serializer = ConsultationRequestSerializer(data=request.data)
    if serializer.is_valid():
        instance = serializer.save()
        
        # Send confirmation email to user
        try:
            user_email = instance.email
            subject = "Consultation Request Received - XSTN"
            message = f"""Thank you for requesting a consultation!

Dear {instance.full_name},

Thank you for your interest in XSTN consultation services. We have received your request and will be in touch shortly.

Consultation Details:
- Consultation Type: {instance.get_consultation_type_display()}
- Preferred Date: {instance.preferred_date or 'Not specified'}
- Requirement: {instance.requirement}

Our team will reach out to you within 24 hours to schedule your consultation session.

Best regards,
XSTN Team - Consultation Services
www.xstn.tech
"""
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email], fail_silently=True)
            
            # Send admin notification
            admin_subject = f"New Consultation Request - {instance.get_consultation_type_display()} from {instance.full_name}"
            admin_message = f"""New Consultation Request received!

Name: {instance.full_name}
Email: {instance.email}
Phone: {instance.phone or 'Not provided'}
Consultation Type: {instance.get_consultation_type_display()}
Preferred Date: {instance.preferred_date or 'Not specified'}
Requirement: {instance.requirement}
Status: {instance.status.title()}

Please log in to admin panel to review: http://localhost:8000/admin/core/consultationrequest/
"""
            send_mail(admin_subject, admin_message, settings.DEFAULT_FROM_EMAIL, [settings.ADMIN_EMAIL], fail_silently=True)
        except Exception as e:
            print(f"Error sending email: {str(e)}")
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def newsletter_subscription_api(request):
    """API endpoint for newsletter subscription"""
    serializer = NewsletterSubscriptionSerializer(data=request.data)
    if serializer.is_valid():
        instance = serializer.save()
        
        # Send confirmation email to user
        try:
            user_email = instance.email
            subject = "Welcome to XSTN Newsletter!"
            message = f"""You've been subscribed to XSTN Newsletter!

Dear Subscriber,

Thank you for subscribing to the XSTN Newsletter. You will now receive updates about:
- Latest projects and case studies
- Industry insights and trends
- Company news and announcements
- Exclusive offers and opportunities

We're excited to share our journey with you!

Best regards,
XSTN Team
www.xstn.tech
"""
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email], fail_silently=True)
            
            # Send admin notification
            admin_subject = f"New Newsletter Subscription - {instance.email}"
            admin_message = f"""New Newsletter Subscription!

Email: {instance.email}
Status: Active
Subscription Date: {instance.created_at}

This subscriber has been added to the mailing list.
"""
            send_mail(admin_subject, admin_message, settings.DEFAULT_FROM_EMAIL, [settings.ADMIN_EMAIL], fail_silently=True)
        except Exception as e:
            print(f"Error sending email: {str(e)}")
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def testimonial_api(request):
    """API endpoint for submitting testimonials"""
    serializer = TestimonialSerializer(data=request.data)
    if serializer.is_valid():
        instance = serializer.save()
        
        # Send confirmation email to user
        try:
            user_email = instance.email
            subject = "Thank you for your testimonial!"
            message = f"""Thank you for your testimonial!

Dear {instance.name},

Thank you for sharing your experience with XSTN. Your feedback is invaluable to us and helps us improve our services.

Your Testimonial:
Rating: {instance.rating}⭐
Message: {instance.message}

We appreciate your support and look forward to working with you in the future!

Best regards,
XSTN Team
www.xstn.tech
"""
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email], fail_silently=True)
            
            # Send admin notification
            admin_subject = f"New Testimonial from {instance.name}"
            admin_message = f"""New Testimonial received!

Name: {instance.name}
Company: {instance.company or 'Not specified'}
Email: {instance.email}
Rating: {instance.rating}⭐
Message: {instance.message}
Status: Awaiting Approval

Please log in to admin panel to approve: http://localhost:8000/admin/core/testimonial/
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
