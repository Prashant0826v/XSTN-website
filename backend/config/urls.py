from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers, status
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model

from apps.users import views as user_views

# Create router for viewsets - only users here, forms are handled by apps.forms.urls
router = routers.DefaultRouter()
router.register(r'users', user_views.UserViewSet, basename='user')

class HealthCheckView(APIView):
    """Health check endpoint"""
    permission_classes = []
    
    def get(self, request):
        return Response({'status': 'healthy', 'message': 'XSTN Django API is running'})

class EmailTokenObtainView(APIView):
    """Custom JWT login that accepts email + password"""
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email') or request.data.get('username', '')
        password = request.data.get('password', '')

        if not email or not password:
            return Response(
                {'detail': 'Email and password are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        User = get_user_model()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {'detail': 'No account found with this email.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if user.is_account_locked():
            return Response(
                {'detail': 'Account is temporarily locked. Try again in 15 minutes.'},
                status=status.HTTP_403_FORBIDDEN
            )

        if not user.is_verified:
            return Response(
                {'detail': 'Please verify your email before logging in.', 'requires_verification': True, 'email': email},
                status=status.HTTP_403_FORBIDDEN
            )

        if not user.check_password(password):
            user.record_failed_login()
            return Response(
                {'detail': 'Invalid password.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        user.reset_failed_login_attempts()
        refresh = RefreshToken.for_user(user)

        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        })

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API Auth - JWT tokens (email-based login)
    path('api/token/', EmailTokenObtainView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # API Routes - users
    path('api/', include(router.urls)),
    
    # Core app URLs (form submissions with email notifications)
    path('', include('core.urls')),
    
    # Forms app URLs (REST API viewsets with email verification)
    path('api/forms/', include('apps.forms.urls')),
    
    # Health check
    path('health/', HealthCheckView.as_view(), name='health'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
