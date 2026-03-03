from django.db import models
import uuid
from django.utils import timezone
from datetime import timedelta


class VerifiableFormMixin(models.Model):
    """Abstract mixin that adds email verification fields and methods to form models."""
    is_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=255, unique=True, null=True, blank=True)
    verification_token_created_at = models.DateTimeField(null=True, blank=True)
    verified_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def generate_verification_token(self):
        """Generate a unique verification token"""
        self.verification_token = str(uuid.uuid4())
        self.verification_token_created_at = timezone.now()
        self.save()
        return self.verification_token

    def is_verification_token_valid(self):
        """Check if verification token is still valid (24 hours)"""
        if not self.verification_token or not self.verification_token_created_at:
            return False
        expiry_time = self.verification_token_created_at + timedelta(hours=24)
        return timezone.now() < expiry_time

    def verify_email(self):
        """Mark form as verified"""
        if self.is_verification_token_valid():
            self.is_verified = True
            self.verified_at = timezone.now()
            self.save()
            return True
        return False


class ContactForm(VerifiableFormMixin):
    """Contact form submission model"""
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Form'
        verbose_name_plural = 'Contact Forms'

    def __str__(self):
        return f"{self.name} - {self.subject}"


class InquiryForm(VerifiableFormMixin):
    """Project inquiry/proposal form model"""
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
        ordering = ['-created_at']
        verbose_name = 'Inquiry Form'
        verbose_name_plural = 'Inquiry Forms'

    def __str__(self):
        return f"{self.name} - {self.project_type}"


class InternshipApplication(VerifiableFormMixin):
    """Internship application model"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('selected', 'Selected'),
        ('rejected', 'Rejected'),
    ]

    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    university = models.CharField(max_length=255)
    skills = models.TextField()
    experience = models.TextField(blank=True, null=True)
    portfolio_url = models.URLField(blank=True, null=True)
    resume_url = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Internship Application'
        verbose_name_plural = 'Internship Applications'

    def __str__(self):
        return f"{self.full_name} - {self.status}"


class DeveloperApplication(VerifiableFormMixin):
    """Developer joining application model"""
    EXPERIENCE_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
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
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('reviewed', 'Reviewed'), ('selected', 'Selected'), ('rejected', 'Rejected')], default='pending')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Developer Application'
        verbose_name_plural = 'Developer Applications'

    def __str__(self):
        return f"{self.full_name} - {self.role_interested}"


class JoinApplication(VerifiableFormMixin):
    """General join XSTN application model"""
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    role_interested = models.CharField(max_length=255)
    why_join = models.TextField()
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('reviewed', 'Reviewed'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Join Application'
        verbose_name_plural = 'Join Applications'

    def __str__(self):
        return f"{self.full_name} - {self.role_interested}"


class ConsultationRequest(VerifiableFormMixin):
    """Consultation request model"""
    CONSULTATION_TYPES = [
        ('website', 'Website Consultation'),
        ('app', 'App Development Consultation'),
        ('ui_ux', 'UI/UX Consultation'),
        ('business', 'Business Idea Discussion'),
        ('other', 'Other'),
    ]

    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    consultation_type = models.CharField(max_length=50, choices=CONSULTATION_TYPES)
    preferred_date = models.DateTimeField(blank=True, null=True)
    requirement = models.TextField()
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('scheduled', 'Scheduled'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='pending')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Consultation Request'
        verbose_name_plural = 'Consultation Requests'

    def __str__(self):
        return f"{self.full_name} - {self.consultation_type} - {self.status}"


class NewsletterSubscription(models.Model):
    """Newsletter subscription model"""
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Newsletter Subscription'
        verbose_name_plural = 'Newsletter Subscriptions'

    def __str__(self):
        return self.email


class Testimonial(VerifiableFormMixin):
    """Client testimonial/review model"""
    name = models.CharField(max_length=255)
    company = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField()
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], default=5)
    message = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Testimonial'
        verbose_name_plural = 'Testimonials'

    def __str__(self):
        return f"{self.name} - {self.rating}★"
