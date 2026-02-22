from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

router = DefaultRouter()
router.register(r'joincommunity', views.JoinCommunityViewSet)
router.register(r'internship', views.InternshipApplicationViewSet)
router.register(r'contact', views.ContactMessageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # Alternative simple endpoints for form submissions
    path('api/join/', views.join_community_api, name='join-api'),
    path('api/internship/', views.internship_application_api, name='internship-api'),
    path('api/contact/', views.contact_message_api, name='contact-api'),
    # Authentication endpoints
    path('auth/register/', views.register_user, name='register'),
    path('auth/login/', views.login_user, name='login'),
    path('auth/profile/', views.get_user_profile, name='profile'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]
