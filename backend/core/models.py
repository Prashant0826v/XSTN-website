from django.db import models
import uuid
from django.utils import timezone
from datetime import timedelta

class JoinCommunity(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    role = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


class InternshipApplication(models.Model):
    POSITION_CHOICES = [
        ('frontend', 'Frontend Developer'),
        ('backend', 'Backend Developer'),
        ('fullstack', 'Full Stack Developer'),
        ('ui_ux', 'UI/UX Designer'),
        ('data_science', 'Data Scientist'),
    ]
    
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    position = models.CharField(max_length=50, choices=POSITION_CHOICES)
    experience = models.TextField()
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    cover_letter = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.full_name} - {self.position}"


class ContactMessage(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.full_name} - {self.subject}"


class ProposalForm(models.Model):
    """Project proposal/inquiry form model"""
    name = models.CharField(max_length=255)
    email = models.EmailField()
    company = models.CharField(max_length=255, blank=True, null=True)
    project_type = models.CharField(max_length=255)
    budget_range = models.CharField(max_length=100, blank=True, null=True)
    timeline = models.CharField(max_length=100, blank=True, null=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Proposal Form'
        verbose_name_plural = 'Proposal Forms'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.project_type}"


class DeveloperApplication(models.Model):
    """Developer joining application model"""
    EXPERIENCE_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('selected', 'Selected'),
        ('rejected', 'Rejected'),
    ]

    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    role_interested = models.CharField(max_length=255)
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='intermediate')
    skills = models.TextField()
    portfolio_url = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Developer Application'
        verbose_name_plural = 'Developer Applications'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} - {self.role_interested}"


class ConsultationRequest(models.Model):
    """Consultation request model"""
    CONSULTATION_TYPES = [
        ('website', 'Website Consultation'),
        ('app', 'App Development Consultation'),
        ('ui_ux', 'UI/UX Consultation'),
        ('business', 'Business Idea Discussion'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    consultation_type = models.CharField(max_length=50, choices=CONSULTATION_TYPES)
    preferred_date = models.DateTimeField(blank=True, null=True)
    requirement = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Consultation Request'
        verbose_name_plural = 'Consultation Requests'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} - {self.consultation_type}"


class NewsletterSubscription(models.Model):
    """Newsletter subscription model"""
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Newsletter Subscription'
        verbose_name_plural = 'Newsletter Subscriptions'
        ordering = ['-created_at']

    def __str__(self):
        return self.email


class Testimonial(models.Model):
    """Client testimonial/review model"""
    name = models.CharField(max_length=255)
    company = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField()
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], default=5)
    message = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Testimonial'
        verbose_name_plural = 'Testimonials'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.rating}★"