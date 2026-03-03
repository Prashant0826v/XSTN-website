from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import (
    ContactFormViewSet, InquiryFormViewSet, InternshipApplicationViewSet,
    DeveloperApplicationViewSet, JoinApplicationViewSet, ConsultationRequestViewSet,
    NewsletterSubscriptionViewSet, TestimonialViewSet, HealthCheckView
)

# Create router and register viewsets
router = SimpleRouter()
router.register(r'contact-forms', ContactFormViewSet, basename='contact-form')
router.register(r'inquiry-forms', InquiryFormViewSet, basename='inquiry-form')
router.register(r'internship-applications', InternshipApplicationViewSet, basename='internship-application')
router.register(r'developer-applications', DeveloperApplicationViewSet, basename='developer-application')
router.register(r'join-applications', JoinApplicationViewSet, basename='join-application')
router.register(r'consultation-requests', ConsultationRequestViewSet, basename='consultation-request')
router.register(r'newsletter-subscriptions', NewsletterSubscriptionViewSet, basename='newsletter-subscription')
router.register(r'testimonials', TestimonialViewSet, basename='testimonial')
router.register(r'health', HealthCheckView, basename='health-check')

urlpatterns = [
    path('', include(router.urls)),
]
