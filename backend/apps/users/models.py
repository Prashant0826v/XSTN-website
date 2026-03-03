from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import secrets

class User(AbstractUser):
    """Extended User model with enhanced security features"""
    
    # Contact info
    phone = models.CharField(max_length=20, blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    
    # Email verification
    is_verified = models.BooleanField(default=False)
    email_verification_code = models.CharField(max_length=6, blank=True, null=True)
    email_verification_expires = models.DateTimeField(blank=True, null=True)
    email_verified_at = models.DateTimeField(blank=True, null=True)
    
    # Password reset
    password_reset_token = models.CharField(max_length=100, blank=True, null=True, unique=True)
    password_reset_expires = models.DateTimeField(blank=True, null=True)
    
    # Security
    failed_login_attempts = models.IntegerField(default=0)
    locked_until = models.DateTimeField(blank=True, null=True)
    last_login_ip = models.GenericIPAddressField(blank=True, null=True)
    last_login_device = models.CharField(max_length=255, blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_activity = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['email_verification_code']),
            models.Index(fields=['password_reset_token']),
        ]

    def __str__(self):
        return self.email

    def generate_verification_code(self):
        """Generate a 6-digit verification code"""
        self.email_verification_code = ''.join([str(secrets.randbelow(10)) for _ in range(6)])
        self.email_verification_expires = timezone.now() + timezone.timedelta(minutes=15)
        return self.email_verification_code

    def generate_password_reset_token(self):
        """Generate a secure password reset token"""
        self.password_reset_token = secrets.token_urlsafe(50)
        self.password_reset_expires = timezone.now() + timezone.timedelta(hours=1)
        return self.password_reset_token

    def is_verification_code_valid(self, code):
        """Check if verification code is valid and not expired"""
        if not self.email_verification_expires:
            return False
        if timezone.now() > self.email_verification_expires:
            return False
        return self.email_verification_code == code

    def is_password_reset_token_valid(self, token):
        """Check if password reset token is valid and not expired"""
        if not self.password_reset_expires:
            return False
        if timezone.now() > self.password_reset_expires:
            return False
        return self.password_reset_token == token

    def is_account_locked(self):
        """Check if account is locked due to failed login attempts"""
        if self.locked_until and timezone.now() < self.locked_until:
            return True
        return False

    def record_failed_login(self):
        """Record a failed login attempt"""
        self.failed_login_attempts += 1
        
        # Lock account after 5 failed attempts for 15 minutes
        if self.failed_login_attempts >= 5:
            self.locked_until = timezone.now() + timezone.timedelta(minutes=15)
        
        self.save()

    def reset_failed_login_attempts(self):
        """Reset failed login counter on successful login"""
        self.failed_login_attempts = 0
        self.locked_until = None
        self.last_activity = timezone.now()
        self.save()

    def verify_email(self):
        """Mark email as verified"""
        self.is_verified = True
        self.email_verification_code = None
        self.email_verification_expires = None
        self.email_verified_at = timezone.now()
        self.save()

