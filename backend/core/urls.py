from django.urls import path, include
from rest_framework.routers import DefaultRouter
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
]
