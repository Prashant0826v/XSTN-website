from rest_framework import serializers
from .models import JoinCommunity, InternshipApplication, ContactMessage


class JoinCommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = JoinCommunity
        fields = ['id', 'full_name', 'email', 'role', 'message', 'created_at']
        read_only_fields = ['id', 'created_at']


class InternshipApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternshipApplication
        fields = ['id', 'full_name', 'email', 'phone', 'position', 'experience', 'resume', 'cover_letter', 'created_at']
        read_only_fields = ['id', 'created_at']


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['id', 'full_name', 'email', 'subject', 'message', 'phone', 'created_at']
        read_only_fields = ['id', 'created_at']
