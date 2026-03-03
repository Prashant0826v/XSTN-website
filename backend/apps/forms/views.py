from django.core.mail import send_mail
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
import logging

from .models import (
    ContactForm, InquiryForm, InternshipApplication, DeveloperApplication,
    JoinApplication, ConsultationRequest, NewsletterSubscription, Testimonial
)
from .serializers import (
    ContactFormSerializer, InquiryFormSerializer, InternshipApplicationSerializer,
    DeveloperApplicationSerializer, JoinApplicationSerializer, ConsultationRequestSerializer,
    NewsletterSubscriptionSerializer, TestimonialSerializer
)
from .email_notifications import (
    send_verification_email,
    send_admin_notification,
    send_confirmation_email,
    send_approval_email,
    send_rejection_email,
    EmailService
)

logger = logging.getLogger(__name__)


class ContactFormViewSet(viewsets.ModelViewSet):
    """ViewSet for contact forms with email verification"""
    queryset = ContactForm.objects.all()
    serializer_class = ContactFormSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        """
        Create contact form and send verification email
        1. User submits form
        2. Verification email sent with link
        3. User clicks link to verify
        4. Admin notified after verification
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        
        # Generate verification token
        token = instance.generate_verification_token()
        
        # Send verification email to user
        send_verification_email(
            email=instance.email,
            token=token,
            form_type='contact',
            name=instance.name
        )
        
        return Response({
            'message': '✓ Form submitted! Please verify your email to complete the process.',
            'data': serializer.data,
            'next_step': 'Check your email for verification link (valid for 24 hours)'
        }, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        """Save form and return instance"""
        return serializer.save()

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def verify_email(self, request):
        """
        Verify email using token
        After user clicks verification link, token is sent here
        """
        token = request.data.get('token')
        
        if not token:
            return Response(
                {'error': 'Verification token is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            contact_form = ContactForm.objects.get(verification_token=token)
        except ContactForm.DoesNotExist:
            return Response(
                {'error': 'Invalid or expired verification token'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verify email
        if contact_form.verify_email():
            # Send admin notification after verification
            send_admin_notification(ContactFormSerializer(contact_form).data, 'contact')
            
            # Send confirmation email to user
            send_confirmation_email(contact_form.email, contact_form.name, 'contact')
            
            return Response({
                'message': '✓ Email verified successfully! We have received your submission.',
                'verified': True
            }, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'Verification token has expired. Please submit the form again.'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def get_queryset(self):
        """Only admin can view all"""
        if self.request.user.is_staff:
            return ContactForm.objects.all()
        return ContactForm.objects.none()




class InquiryFormViewSet(viewsets.ModelViewSet):
    """ViewSet for inquiry forms with email verification"""
    queryset = InquiryForm.objects.all()
    serializer_class = InquiryFormSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        """Create inquiry and send verification email"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        
        # Generate verification token
        token = instance.generate_verification_token()
        
        # Send verification email
        send_verification_email(
            email=instance.email,
            token=token,
            form_type='inquiry',
            name=instance.name
        )
        
        return Response({
            'message': '✓ Inquiry received! Please verify your email.',
            'data': serializer.data,
            'next_step': 'Check your email for verification link'
        }, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        return serializer.save()

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def verify_email(self, request):
        """Verify email using token"""
        token = request.data.get('token')
        
        if not token:
            return Response({'error': 'Token required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            inquiry = InquiryForm.objects.get(verification_token=token)
        except InquiryForm.DoesNotExist:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        
        if inquiry.verify_email():
            send_admin_notification(InquiryFormSerializer(inquiry).data, 'inquiry')
            send_confirmation_email(inquiry.email, inquiry.name, 'inquiry')
            
            return Response({
                'message': '✓ Email verified! Your proposal request has been received.',
                'verified': True
            }, status=status.HTTP_200_OK)
        
        return Response({'error': 'Token expired'}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        if self.request.user.is_staff:
            return InquiryForm.objects.all()
        return InquiryForm.objects.none()




class InternshipApplicationViewSet(viewsets.ModelViewSet):
    """ViewSet for internship applications with email verification"""
    queryset = InternshipApplication.objects.all()
    serializer_class = InternshipApplicationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        """Create application and send verification email"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        
        # Generate verification token
        token = instance.generate_verification_token()
        
        # Send verification email
        send_verification_email(
            email=instance.email,
            token=token,
            form_type='internship',
            name=instance.full_name
        )
        
        return Response({
            'message': '✓ Application submitted! Please verify your email.',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        return serializer.save()

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def verify_email(self, request):
        """Verify email"""
        token = request.data.get('token')
        
        if not token:
            return Response({'error': 'Token required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            app = InternshipApplication.objects.get(verification_token=token)
        except InternshipApplication.DoesNotExist:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        
        if app.verify_email():
            send_admin_notification(InternshipApplicationSerializer(app).data, 'internship')
            send_confirmation_email(app.email, app.full_name, 'internship')
            
            return Response({
                'message': '✓ Email verified! Your application has been received.',
                'verified': True
            }, status=status.HTTP_200_OK)
        
        return Response({'error': 'Token expired'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail='pk', methods=['post'], permission_classes=[IsAuthenticated])
    def approve(self, request, pk=None):
        """Admin action: Approve application and send email"""
        app = self.get_object()
        app.status = 'selected'
        app.save()
        
        next_steps = request.data.get('next_steps', 
            'We will contact you with interview details and next steps.')
        
        send_approval_email(app.email, app.full_name, 'internship', next_steps)
        
        return Response({'message': '✓ Applicant approved and email sent.'})

    @action(detail='pk', methods=['post'], permission_classes=[IsAuthenticated])
    def reject(self, request, pk=None):
        """Admin action: Reject application and send email"""
        app = self.get_object()
        app.status = 'rejected'
        app.save()
        
        reason = request.data.get('reason', '')
        send_rejection_email(app.email, app.full_name, 'internship', reason)
        
        return Response({'message': '✓ Applicant notified.'})

    def get_queryset(self):
        if self.request.user.is_staff:
            return InternshipApplication.objects.all()
        return InternshipApplication.objects.none()




class DeveloperApplicationViewSet(viewsets.ModelViewSet):
    """ViewSet for developer applications with email verification"""
    queryset = DeveloperApplication.objects.all()
    serializer_class = DeveloperApplicationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        """Create application and send verification email"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        
        # Generate verification token
        token = instance.generate_verification_token()
        
        # Send verification email
        send_verification_email(
            email=instance.email,
            token=token,
            form_type='developer',
            name=instance.full_name
        )
        
        return Response({
            'message': '✓ Application submitted! Please verify your email.',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        return serializer.save()

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def verify_email(self, request):
        """Verify email"""
        token = request.data.get('token')
        
        if not token:
            return Response({'error': 'Token required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            app = DeveloperApplication.objects.get(verification_token=token)
        except DeveloperApplication.DoesNotExist:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        
        if app.verify_email():
            send_admin_notification(DeveloperApplicationSerializer(app).data, 'developer')
            send_confirmation_email(app.email, app.full_name, 'developer')
            
            return Response({
                'message': '✓ Email verified! Your application has been received.',
                'verified': True
            }, status=status.HTTP_200_OK)
        
        return Response({'error': 'Token expired'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail='pk', methods=['post'], permission_classes=[IsAuthenticated])
    def approve(self, request, pk=None):
        """Admin action: Approve application"""
        app = self.get_object()
        app.status = 'selected'
        app.save()
        
        next_steps = request.data.get('next_steps', 
            'Congratulations! Please check your email for onboarding details.')
        
        send_approval_email(app.email, app.full_name, 'developer', next_steps)
        return Response({'message': '✓ Developer approved!'})

    @action(detail='pk', methods=['post'], permission_classes=[IsAuthenticated])
    def reject(self, request, pk=None):
        """Admin action: Reject application"""
        app = self.get_object()
        app.status = 'rejected'
        app.save()
        
        reason = request.data.get('reason', '')
        send_rejection_email(app.email, app.full_name, 'developer', reason)
        return Response({'message': '✓ Developer notified.'})

    def get_queryset(self):
        if self.request.user.is_staff:
            return DeveloperApplication.objects.all()
        return DeveloperApplication.objects.none()



class JoinApplicationViewSet(viewsets.ModelViewSet):
    """ViewSet for join applications with email verification"""
    queryset = JoinApplication.objects.all()
    serializer_class = JoinApplicationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        
        token = instance.generate_verification_token()
        send_verification_email(instance.email, token, 'join', instance.full_name)
        
        return Response({
            'message': '✓ Application submitted! Please verify your email.',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        return serializer.save()

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def verify_email(self, request):
        token = request.data.get('token')
        
        if not token:
            return Response({'error': 'Token required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            app = JoinApplication.objects.get(verification_token=token)
        except JoinApplication.DoesNotExist:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        
        if app.verify_email():
            send_admin_notification(JoinApplicationSerializer(app).data, 'join')
            send_confirmation_email(app.email, app.full_name, 'join')
            
            return Response({'message': '✓ Email verified!', 'verified': True})
        
        return Response({'error': 'Token expired'}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        if self.request.user.is_staff:
            return JoinApplication.objects.all()
        return JoinApplication.objects.none()




class ConsultationRequestViewSet(viewsets.ModelViewSet):
    """ViewSet for consultation requests with email verification"""
    queryset = ConsultationRequest.objects.all()
    serializer_class = ConsultationRequestSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        
        token = instance.generate_verification_token()
        send_verification_email(instance.email, token, 'consultation', instance.full_name)
        
        return Response({
            'message': '✓ Request submitted! Please verify your email.',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        return serializer.save()

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def verify_email(self, request):
        token = request.data.get('token')
        
        if not token:
            return Response({'error': 'Token required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            req = ConsultationRequest.objects.get(verification_token=token)
        except ConsultationRequest.DoesNotExist:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        
        if req.verify_email():
            send_admin_notification(ConsultationRequestSerializer(req).data, 'consultation')
            send_confirmation_email(req.email, req.full_name, 'consultation')
            
            return Response({'message': '✓ Email verified!', 'verified': True})
        
        return Response({'error': 'Token expired'}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        if self.request.user.is_staff:
            return ConsultationRequest.objects.all()
        return ConsultationRequest.objects.none()




class NewsletterSubscriptionViewSet(viewsets.ModelViewSet):
    """ViewSet for newsletter subscriptions"""
    queryset = NewsletterSubscription.objects.all()
    serializer_class = NewsletterSubscriptionSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        """Create newsletter subscription and send confirmation"""
        # Check if email already subscribed
        email = request.data.get('email')
        if NewsletterSubscription.objects.filter(email=email, is_active=True).exists():
            return Response(
                {'message': 'Email already subscribed to newsletter'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Send confirmation email
        send_confirmation_email(email, 'Subscriber', 'newsletter')
        
        return Response(
            {'message': '✓ Successfully subscribed to newsletter!', 'data': serializer.data},
            status=status.HTTP_201_CREATED
        )

    def perform_create(self, serializer):
        return serializer.save()

    @action(detail=True, methods=['post'], permission_classes=[AllowAny])
    def unsubscribe(self, request, pk=None):
        """Unsubscribe from newsletter"""
        try:
            subscription = self.get_object()
            subscription.is_active = False
            subscription.save()
            return Response({'message': '✓ Unsubscribed successfully'})
        except NewsletterSubscription.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    def get_queryset(self):
        if self.request.user.is_staff:
            return NewsletterSubscription.objects.all()
        return NewsletterSubscription.objects.none()




class TestimonialViewSet(viewsets.ModelViewSet):
    """ViewSet for testimonials with email verification"""
    queryset = Testimonial.objects.filter(is_approved=True)
    serializer_class = TestimonialSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        
        token = instance.generate_verification_token()
        send_verification_email(instance.email, token, 'testimonial', instance.name)
        
        return Response({
            'message': '✓ Testimonial submitted! Check your email to verify.',
            'data': serializer.data,
            'note': 'Testimonials appear after admin approval'
        }, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        return serializer.save()

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def verify_email(self, request):
        token = request.data.get('token')
        
        if not token:
            return Response({'error': 'Token required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            testimonial = Testimonial.objects.get(verification_token=token)
        except Testimonial.DoesNotExist:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        
        if testimonial.verify_email():
            send_confirmation_email(testimonial.email, testimonial.name, 'testimonial')
            return Response({'message': '✓ Email verified! Awaiting admin approval.', 'verified': True})
        
        return Response({'error': 'Token expired'}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Testimonial.objects.all()
        return Testimonial.objects.filter(is_approved=True)


class HealthCheckView(viewsets.ViewSet):
    """Health check endpoint"""
    
    @action(detail=False, methods=['get'])
    def get(self, request):
        return Response({'status': 'healthy', 'message': 'XSTN API is running'})

