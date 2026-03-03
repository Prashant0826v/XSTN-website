#!/usr/bin/env python
import os
import django
import json
import requests
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

print("=" * 60)
print("XSTN EMAIL VERIFICATION TEST")
print("=" * 60)
print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# Test 1: Register a new user and check email
print("TEST 1: User Registration")
print("-" * 60)

registration_data = {
    'username': f'testuser_{int(datetime.now().timestamp())}',
    'email': 'testregistration@example.com',
    'password': 'TestPass123',
    'confirm_password': 'TestPass123',
    'first_name': 'Test',
    'last_name': 'User'
}

response = requests.post(
    'http://localhost:8000/api/users/register/',
    json=registration_data
)

print(f"Registration Status: {response.status_code}")
if response.status_code == 201:
    print("✅ Registration successful!")
    data = response.json()
    print(f"Message: {data.get('message')}")
    print("→ Check your email inbox for verification code")
else:
    print(f"❌ Registration failed: {response.text}")

print()
print("TEST 2: Contact Form Submission")
print("-" * 60)

contact_data = {
    'name': 'Test Contact',
    'email': 'testcontact@example.com',
    'phone': '+1234567890',
    'subject': 'Test Email Configuration',
    'message': 'Testing if email is working via contact form'
}

response = requests.post(
    'http://localhost:8000/api/forms/contact/',
    json=contact_data
)

print(f"Contact Form Status: {response.status_code}")
if response.status_code == 201:
    print("✅ Contact form submitted successfully!")
    print("→ Check your email inbox at prashant.iron1@gmail.com for confirmation")
else:
    print(f"❌ Contact form failed: {response.text}")

print()
print("TEST 3: Check Email Configuration")
print("-" * 60)

from django.conf import settings
from pathlib import Path

env_file = Path(__file__).parent / '.env'
if env_file.exists():
    with open(env_file) as f:
        content = f.read()
        has_smtp = 'SMTP_USER=' in content and 'SMTP_PASSWORD=' in content
        print(f"✅ .env file exists" if has_smtp else "❌ Email config missing")
        
        # Show configuration (without exposing full password)
        for line in content.split('\n'):
            if 'SMTP_USER=' in line:
                print(f"  {line}")
            elif 'SMTP_SERVER=' in line:
                print(f"  {line}")
            elif 'SMTP_PORT=' in line:
                print(f"  {line}")

print()
print("EMAIL_BACKEND:", settings.EMAIL_BACKEND)
print("EMAIL_HOST:", settings.EMAIL_HOST if hasattr(settings, 'EMAIL_HOST') else 'N/A')
print("EMAIL_PORT:", settings.EMAIL_PORT if hasattr(settings, 'EMAIL_PORT') else 'N/A')

print()
print("=" * 60)
print("✅ EMAIL VERIFICATION COMPLETE")
print("=" * 60)
print()
print("📧 NEXT STEPS:")
print("1. Check prashant.iron1@gmail.com inbox")
print("2. Look for:")
print("   - Verification email (from registration)")
print("   - Contact form confirmation email")
print("3. If you don't see emails within 2 minutes:")
print("   - Check spam/junk folder")
print("   - Verify app password in Google Account")
print("   - Check Django server logs for errors")
print()
