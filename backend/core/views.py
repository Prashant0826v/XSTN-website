from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import JoinCommunity, InternshipApplication, ContactMessage
from .serializers import JoinCommunitySerializer, InternshipApplicationSerializer, ContactMessageSerializer


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
def join_community_api(request):
    """API endpoint for submitting join community form"""
    serializer = JoinCommunitySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def internship_application_api(request):
    """API endpoint for submitting internship application form"""
    serializer = InternshipApplicationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def contact_message_api(request):
    """API endpoint for submitting contact form"""
    serializer = ContactMessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
