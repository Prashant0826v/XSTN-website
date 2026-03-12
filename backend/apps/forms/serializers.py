from rest_framework import serializers
from .models import (
    ContactForm, 
    InquiryForm, 
    InternshipApplication, 
    DeveloperApplication,
    JoinApplication,
    ConsultationRequest,
    NewsletterSubscription,
    Testimonial
)

class ContactFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactForm
        fields = ['id', 'name', 'email', 'phone', 'subject', 'message', 'is_read', 'created_at']
        read_only_fields = ['id', 'created_at']

class InquiryFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = InquiryForm
        fields = ['id', 'name', 'email', 'company', 'project_type', 'budget_range', 'timeline', 'message', 'is_read', 'created_at']
        read_only_fields = ['id', 'created_at']

class InternshipApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternshipApplication
        fields = ['id', 'full_name', 'email', 'phone', 'university', 'skills', 'experience', 'portfolio_url', 'resume_url', 'status', 'notes', 'is_read', 'created_at']
        read_only_fields = ['id', 'created_at']

class DeveloperApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeveloperApplication
        fields = ['id', 'full_name', 'email', 'phone', 'role_interested', 'experience_level', 'skills', 'portfolio_url', 'github_url', 'resume_url', 'message', 'status', 'is_read', 'created_at']
        read_only_fields = ['id', 'created_at']

class JoinApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JoinApplication
        fields = ['id', 'full_name', 'email', 'role_interested', 'why_join', 'status', 'is_read', 'created_at']
        read_only_fields = ['id', 'created_at']

class ConsultationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultationRequest
        fields = ['id', 'full_name', 'email', 'phone', 'consultation_type', 'preferred_date', 'requirement', 'status', 'is_read', 'created_at']
        read_only_fields = ['id', 'created_at']

class NewsletterSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscription
        fields = ['id', 'email', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ['id', 'name', 'company', 'email', 'rating', 'message', 'is_approved', 'created_at']

