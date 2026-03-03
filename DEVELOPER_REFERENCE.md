# XSTN Quick Reference Guide

Fast reference for developers and admins implementing email verification system.

---

## 🚀 Quick Start

### 1. Check Backend Status
```bash
cd backend
python manage.py test        # Run tests (should pass all 64+)
python manage.py migrate     # Apply migrations
python manage.py runserver   # Start development server
```

### 2. Test Email Verification
```bash
# In Django shell
python manage.py shell

# Create test form
from apps.forms.models import ContactForm
form = ContactForm.objects.create(
    name="Test User",
    email="test@example.com",
    phone="123456",
    subject="Test",
    message="Test message"
)

# Generate token
token = form.generate_verification_token()
print(f"Token: {token}")

# Check if valid
print(f"Valid: {form.is_verification_token_valid()}")

# Verify email
form.verify_email()
print(f"Verified: {form.is_verified}")
```

---

## 📧 Email Configuration

### In Django Settings (config/settings.py)

```python
# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'          # or your email provider
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'  # Use app-specific password
DEFAULT_FROM_EMAIL = 'noreply@xstn.com'    # Sender email

# Admin email for notifications
ADMIN_EMAIL = 'admin@xstn.com'
```

### Environment Variables (.env)

```
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
ADMIN_EMAIL=admin@xstn.com
SECRET_KEY=your-secret-key-here
```

---

## 📝 API Quick Reference

### Submit Form & Get Verification Prompt

```bash
POST /api/contact/
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "subject": "Hello",
  "message": "Message text"
}

Response (201):
{
  "message": "✓ Form submitted! Please verify your email.",
  "data": {...},
  "next_step": "Check your email for verification link (valid for 24 hours)"
}
```

### Verify Email with Token

```bash
POST /api/contact/verify_email/
Content-Type: application/json

{
  "token": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"
}

Response (200):
{
  "message": "✓ Email verified successfully!",
  "verified": true
}
```

### Admin Approve Application

```bash
POST /api/internship/1/approve/
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "next_steps": "Join orientation Monday at 10 AM"
}

Response:
{
  "message": "✓ Applicant approved and email sent."
}
```

### Admin Reject Application

```bash
POST /api/internship/1/reject/
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "reason": "Selected other candidates"
}

Response:
{
  "message": "✓ Applicant notified."
}
```

---

## 🔑 Authentication (JWT Tokens)

### Get Tokens

```bash
POST /api/token/
Content-Type: application/json

{
  "username": "admin",
  "password": "password"
}

Response:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Use Access Token

```bash
GET /api/contact/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

### Refresh Token

```bash
POST /api/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}

Response:
{
  "access": "new-access-token-here"
}
```

---

## 📚 File Locations

### Backend Files

| Component | File |
|-----------|------|
| Views (API) | `backend/apps/forms/views.py` |
| Models | `backend/apps/forms/models.py` |
| Email Service | `backend/apps/forms/email_notifications.py` |
| Serializers | `backend/apps/forms/serializers.py` |
| Admin | `backend/apps/forms/admin.py` |
| Tests | `backend/apps/forms/tests.py` |
| Settings | `backend/config/settings.py` |

### Documentation

| Topic | File |
|-------|------|
| Security Features | `backend/SECURITY.md` |
| API with Verification | `backend/API_EMAIL_VERIFICATION.md` |
| Frontend Integration | `frontend/EMAIL_VERIFICATION_GUIDE.md` |
| Project Summary | `PROJECT_SUMMARY.md` |

---

## 🐛 Debugging Tips

### Email Not Sending?

```bash
# Test email configuration
python manage.py shell

from django.core.mail import send_mail
from django.conf import settings

send_mail(
    'Test Email',
    'This is a test.',
    settings.DEFAULT_FROM_EMAIL,
    ['your-email@test.com'],
    fail_silently=False,
)
```

### Token Validation Issues?

```python
from apps.forms.models import ContactForm
from django.utils import timezone
from datetime import timedelta

form = ContactForm.objects.get(id=1)

# Check token
print(f"Token: {form.verification_token}")
print(f"Created at: {form.verification_token_created_at}")
print(f"Current time: {timezone.now()}")

# Calculate expiry
expiry = form.verification_token_created_at + timedelta(hours=24)
print(f"Expires at: {expiry}")
print(f"Is valid: {form.is_verification_token_valid()}")
```

### View Admin Submissions

```python
from apps.forms.models import ContactForm

# All submissions
all_forms = ContactForm.objects.all()

# Verified only
verified = ContactForm.objects.filter(is_verified=True)

# Unverified (pending)
pending = ContactForm.objects.filter(is_verified=False)

# With details
for form in all_forms:
    print(f"ID: {form.id}, Email: {form.email}, Verified: {form.is_verified}")
```

---

## 📊 Models Quick Reference

### All Form Models Have These Fields:

```python
id                              # Auto-increment primary key
created_at                      # Timestamp when submitted
updated_at                      # Timestamp when updated
is_verified                     # Boolean (default False)
verification_token             # UUID hex string (32 chars)
verification_token_created_at  # When token was generated
verified_at                     # When email was verified
```

---

## 🔒 Security Checklist

### Before Going Live:

- [ ] Email credentials configured (not in code)
- [ ] DEBUG = False in production
- [ ] ALLOWED_HOSTS configured with domain
- [ ] SECRET_KEY is strong (50+ chars)
- [ ] SECURE_SSL_REDIRECT = True
- [ ] CORS_ALLOWED_ORIGINS set correctly
- [ ] Token expiration tested (24 hours)
- [ ] Admin notifications working
- [ ] All tests passing
- [ ] Email logs monitored

---

## 🧪 Common Test Commands

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test apps.forms

# Run specific test class
python manage.py test apps.forms.tests.ContactFormTestCase

# Run specific test method
python manage.py test apps.forms.tests.ContactFormTestCase.test_create_form

# Run with verbose output
python manage.py test -v 2

# Run with coverage report
coverage run --source='apps' manage.py test
coverage report
coverage html  # Creates htmlcov/index.html
```

---

## 💾 Database Commands

```bash
# Create migrations
python manage.py makemigrations

# Show migration SQL
python manage.py sqlmigrate apps.forms 0001

# Apply migrations
python manage.py migrate

# Rollback migrations
python manage.py migrate apps.forms 0001

# Clear all data
python manage.py flush

# Dump data to JSON
python manage.py dumpdata > data.json

# Load data from JSON
python manage.py loaddata data.json
```

---

## 📱 Frontend Implementation Checklist

### Verification Page Setup:

- [ ] Create `verify-email.html` page
- [ ] Add `verify-email.js` script
- [ ] Add CSS styling
- [ ] Extract token from URL query params
- [ ] Call verification endpoint
- [ ] Show loading indicator
- [ ] Display success/error messages
- [ ] Redirect on success
- [ ] Store pending verification in localStorage
- [ ] Test with all form types

---

## 🚨 Error Responses Quick Reference

| Code | Error | Cause |
|------|-------|-------|
| 200 | Email verified successfully | Valid token, status 200 |
| 201 | Form submitted | Form created, status 201 |
| 400 | Invalid token | Token doesn't exist or malformed |
| 400 | Token expired | Token older than 24 hours |
| 400 | Token required | No token in request body |
| 401 | Unauthorized | Missing authentication header |
| 403 | Forbidden | Non-staff trying admin action |
| 404 | Not found | Token or form doesn't exist |
| 500 | Server error | Email service failure |

---

## 📞 Request Headers Format

```bash
# Public endpoint (no auth needed)
GET /api/contact/
Content-Type: application/json

# Admin endpoint (requires auth)
GET /api/contact/
Authorization: Bearer <access_token>
Content-Type: application/json

# Form submission (no auth needed)
POST /api/contact/
Content-Type: application/json
```

---

## 🔄 Verification Flow Quick Summary

```
1. User submits form on website
2. Backend receives form data
3. Form saved to database (is_verified: false)
4. UUID token generated (32 chars, random)
5. Verification email sent with token link
6. User clicks link in email (within 24 hours)
7. Frontend sends token to backend
8. Backend validates token (checks expiry)
9. Form marked as verified (is_verified: true)
10. Admin notified of submission
11. Confirmation email sent to user
12. Token cleared from database
```

---

## 🎯 All 8 Form Types

1. **ContactForm** - General inquiries
2. **InquiryForm** - Business proposals
3. **InternshipApplication** - Internship applications
4. **DeveloperApplication** - Developer recruitment
5. **JoinApplication** - Join as partner/founder
6. **ConsultationRequest** - Consultation bookings
7. **NewsletterSubscription** - Newsletter signup
8. **Testimonial** - Client testimonials

---

## 📖 Documentation Map

```
XSTN Project/
├── PROJECT_SUMMARY.md              ← Start here (overview)
├── DEVELOPER_REFERENCE.md          ← This file (quick reference)
├── backend/
│   ├── SECURITY.md                 ← Security features
│   ├── API_EMAIL_VERIFICATION.md   ← API endpoints
│   ├── README.md                   ← Backend setup
│   └── requirements.txt            ← Dependencies
└── frontend/
    ├── EMAIL_VERIFICATION_GUIDE.md ← Frontend implementation
    └── README.md                   ← Frontend setup
```

---

## 🎓 Where to Find Answers

| Question | File |
|----------|------|
| How does verification work? | SECURITY.md section 3 |
| What are the API endpoints? | API_EMAIL_VERIFICATION.md |
| How to set up frontend? | EMAIL_VERIFICATION_GUIDE.md |
| How to implement email? | API_EMAIL_VERIFICATION.md section 1 |
| How is password hashing done? | SECURITY.md section 2 |
| How to fix email issues? | This file - Debugging Tips |
| What security features exist? | SECURITY.md sections 1-14 |

---

## 🏁 Success Indicators

The implementation is working correctly when:

- ✅ All pytest tests pass (64+)
- ✅ Form submissions return success message
- ✅ Verification emails arrive within 5 seconds
- ✅ Token validation works (accepts within 24h, rejects after)
- ✅ Admin receives notification emails
- ✅ User receives confirmation emails
- ✅ Admin can approve/reject applications
- ✅ Status changes trigger correct emails
- ✅ Tokens are one-time use
- ✅ Dashboard shows all submissions

---

**Version**: 1.0  
**Last Updated**: 2024  
**Status**: ✅ Ready to Deploy
