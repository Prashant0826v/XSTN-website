import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.conf import settings

print("Email Configuration:")
print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
print(f"EMAIL_HOST: {settings.EMAIL_HOST if hasattr(settings, 'EMAIL_HOST') else 'Not set'}")
print(f"EMAIL_PORT: {settings.EMAIL_PORT if hasattr(settings, 'EMAIL_PORT') else 'Not set'}")
print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER if hasattr(settings, 'EMAIL_HOST_USER') else 'Not set'}")
print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
print(f"ADMIN_EMAIL: {settings.ADMIN_EMAIL}")
