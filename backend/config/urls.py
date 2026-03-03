from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users import views as user_views
from apps.forms import views as form_views

# Create router for viewsets
router = routers.DefaultRouter()
router.register(r'users', user_views.UserViewSet, basename='user')
router.register(r'forms/contact', form_views.ContactFormViewSet, basename='contact')
router.register(r'forms/inquiry', form_views.InquiryFormViewSet, basename='inquiry')
router.register(r'forms/internship', form_views.InternshipApplicationViewSet, basename='internship')
router.register(r'forms/developer', form_views.DeveloperApplicationViewSet, basename='developer')
router.register(r'forms/join', form_views.JoinApplicationViewSet, basename='join')
router.register(r'forms/consultation', form_views.ConsultationRequestViewSet, basename='consultation')
router.register(r'forms/newsletter', form_views.NewsletterSubscriptionViewSet, basename='newsletter')
router.register(r'forms/testimonials', form_views.TestimonialViewSet, basename='testimonial')

class HealthCheckView(APIView):
    """Health check endpoint"""
    def get(self, request):
        return Response({'status': 'healthy', 'message': 'XSTN Django API is running'})

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API Auth
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # API Routes
    path('api/', include(router.urls)),
    
    # Core app URLs (form submissions with email notifications)
    path('', include('core.urls')),
    
    # Forms app URLs
    path('api/forms/', include('apps.forms.urls')),
    
    # Health check
    path('health/', HealthCheckView.as_view(), name='health'),
    path('', HealthCheckView.as_view(), name='root'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
