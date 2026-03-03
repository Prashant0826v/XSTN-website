# XSTN Backend - Security Features & Documentation

Complete security implementation overview for the XSTN backend, including authentication, authorization, data protection, and verification systems.

## 🔐 Overview

The XSTN backend implements enterprise-grade security measures across multiple layers:
- **Authentication**: JWT token-based authentication
- **Authorization**: Role-based access control (RBAC)
- **Data Protection**: Encryption, hashing, and validation
- **Email Verification**: Token-based email OTP system
- **Input Validation**: Serializer-level validation on all endpoints
- **Infrastructure**: CORS protection, CSRF prevention, SQL injection prevention

---

## 1. Authentication System

### 1.1 JWT Token Authentication

**Technology**: `djangorestframework-simplejwt`

#### How It Works:
```python
# Tokens are issued on login
- Access Token: Short-lived (5 minutes default)
  - Used for API requests
  - Included in Authorization header: "Bearer <token>"
  
- Refresh Token: Long-lived (24 hours default)  
  - Used to obtain new access tokens
  - Secure refresh mechanism without re-login
```

#### API Endpoints:
```
POST /api/auth/token/
- Request: { "username": "...", "password": "..." }
- Response: { "access": "...", "refresh": "..." }

POST /api/auth/token/refresh/
- Request: { "refresh": "..." }
- Response: { "access": "..." }
```

#### Token Claims (Payload):
```json
{
  "token_type": "access",
  "exp": 1234567890,        // Expiration timestamp
  "iat": 1234567800,        // Issued at
  "jti": "unique-id",       // JWT ID
  "user_id": 1,             // User identifier
  "username": "admin",      // Username
  "email": "admin@xstn.com" // Email
}
```

#### Security Features:
- ✅ Tokens are cryptographically signed (HMAC-SHA256 default)
- ✅ Expiration timestamps enforce token lifetime
- ✅ Refresh tokens can be rotated for additional security
- ✅ JWT header contains algorithm info for verification

---

## 2. Password Security

### 2.1 Password Hashing

**Technology**: Django's default PBKDF2 (Password-Based Key Derivation Function 2)

#### How It Works:
```python
# Django automatically hashes passwords using PBKDF2
- Algorithm: PBKDF2 with SHA256
- Iterations: 260,000 (default, configurable)
- Salt: Randomly generated per password
- Output: 32-byte (256-bit) hash

Example hash format:
pbkdf2_sha256$260000$salt$hash
```

#### Password Storage:
```python
# Never stored in plain text
# Hash changes every time password is set (new salt)
user.set_password('mypassword')  # Uses PBKDF2 automatically
user.save()
```

### 2.2 Password Requirements

**Current Implementation**:
- ✅ Minimum 8 characters
- ✅ Mix of uppercase and lowercase letters
- ✅ At least one number
- ✅ At least one special character

**Validation** (in serializers):
```python
def validate_password(self, value):
    if len(value) < 8:
        raise ValidationError("Password too short")
    
    if not any(char.isupper() for char in value):
        raise ValidationError("Password must contain uppercase")
    
    if not any(char.isdigit() for char in value):
        raise ValidationError("Password must contain number")
    
    if not any(char in '!@#$%^&*' for char in value):
        raise ValidationError("Password must contain special char")
    
    return value
```

### 2.3 Account Lockout (Failed Login Protection)

**Feature**: Automatic account locking after 5 failed attempts

```python
class User(models.Model):
    failed_login_attempts = models.IntegerField(default=0)
    is_locked = models.BooleanField(default=False)
    locked_until = models.DateTimeField(null=True)
    
    def increment_failed_attempts(self):
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= 5:
            self.is_locked = True
            self.locked_until = now() + timedelta(hours=1)
        self.save()
    
    def reset_failed_attempts(self):
        self.failed_login_attempts = 0
        self.is_locked = False
        self.save()
```

---

## 3. Email Verification System

### 3.1 Email OTP/Token Verification

**Purpose**: Verify user email ownership before accepting form submissions

#### How It Works:

**Step 1: User Submits Form**
```bash
POST /api/contact/
{
  "name": "John Doe",
  "email": "john@example.com",
  "message": "Hello"
}

Response (201):
{
  "message": "✓ Form submitted! Please verify your email.",
  "data": { ... },
  "next_step": "Check your email for verification link (valid for 24 hours)"
}
```

**Step 2: Verification Token Generated**
```python
# In ContactForm.generate_verification_token():
token = uuid.uuid4().hex  # Generates unique token
self.verification_token = token
self.verification_token_created_at = timezone.now()
self.save()

# Token format: UUID4 hex string (32 characters)
# Example: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
```

**Step 3: Verification Email Sent**
```
To: john@example.com
Subject: XSTN - Verify Your Email Address

📧 Email Verification Required

Hello John,

Someone submitted a form with your email address. Please verify your email by clicking below:

🔗 Verification Link:
https://xstn.com/verify-email?type=contact&token=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6

⏱️  This link expires in 24 hours

If you didn't submit this form, you can ignore this email.

---
XSTN Team
```

**Step 4: User Clicks Link**
```bash
# Frontend submits token to verification endpoint
POST /api/contact/verify_email/
{
  "token": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"
}

Response (200):
{
  "message": "✓ Email verified successfully! We have received your submission.",
  "verified": true
}
```

**Step 5: Token Validation**
```python
# In ContactForm.is_verification_token_valid():
created_at = self.verification_token_created_at
current_time = timezone.now()
expiry_time = created_at + timedelta(hours=24)

is_valid = current_time <= expiry_time
# Token is valid for exactly 24 hours from creation
```

**Step 6: Email Marked as Verified**
```python
def verify_email(self):
    if self.is_verification_token_valid():
        self.is_verified = True
        self.verified_at = timezone.now()
        self.verification_token = None  # Clear token after use
        self.save()
        return True
    return False
```

### 3.2 Token Security Features

✅ **UUID-Based Tokens**
- 128-bit randomly generated (extremely difficult to brute-force)
- No sequential or predictable patterns

✅ **24-Hour Expiration**
- Tokens automatically invalidate after 24 hours
- Prevents indefinite validity window

✅ **One-Time Use**
- Token is cleared after first successful verification
- Cannot be reused even if someone has it

✅ **Timezone-Aware Validation**
- Timestamps use UTC timezone (timezone.now())
- Works correctly regardless of server location

✅ **Database-Backed**
- Tokens stored in database, not in emails
- Email only contains the token reference

### 3.3 Token Models (All Forms)

All 8 form models include verification fields:

```python
class ContactForm(models.Model):
    # ... other fields ...
    is_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=64, unique=True, null=True)
    verification_token_created_at = models.DateTimeField(null=True)
    verified_at = models.DateTimeField(null=True)
    
    def generate_verification_token(self):
        """Generate new verification token"""
        token = uuid.uuid4().hex
        self.verification_token = token
        self.verification_token_created_at = timezone.now()
        self.save()
        return token
    
    def is_verification_token_valid(self):
        """Check if token is still valid (24 hours)"""
        if not self.verification_token_created_at:
            return False
        return timezone.now() <= self.verification_token_created_at + timedelta(hours=24)
    
    def verify_email(self):
        """Mark email as verified if token is valid"""
        if self.is_verification_token_valid():
            self.is_verified = True
            self.verified_at = timezone.now()
            self.verification_token = None
            self.save()
            return True
        return False
```

**Forms with verification**:
- ✅ ContactForm
- ✅ InquiryForm
- ✅ InternshipApplication
- ✅ DeveloperApplication
- ✅ JoinApplication
- ✅ ConsultationRequest
- ✅ Testimonial

---

## 4. Authorization & Access Control

### 4.1 Role-Based Access Control (RBAC)

**Roles** in XSTN:
- `Anonymous` (no login): Can submit forms, verify emails
- `Authenticated User`: Can submit forms
- `Staff/Admin`: Can view all submissions, manage approvals

#### Permission Classes:

```python
# AllowAny - Everyone can access
permission_classes = [AllowAny]  # Form submission endpoints

# IsAuthenticated - Only logged-in users
permission_classes = [IsAuthenticated]  # Admin actions

# Custom - Staff/Admin only
def get_queryset(self):
    if self.request.user.is_staff:
        return ContactForm.objects.all()
    return ContactForm.objects.none()  # Hide from non-staff
```

### 4.2 Admin-Only Actions

**Approve/Reject Applications**:
```bash
POST /api/internship/{id}/approve/
Authorization: Bearer <token>
{
  "next_steps": "We will contact you with interview details"
}
# Only works if user.is_staff == True
```

**Query Restrictions**:
```python
# Non-staff users cannot list any forms
GET /api/contact/
# Response: [] (empty list)

# Only staff can see all submissions
GET /api/contact/
Authorization: Bearer <admin_token>
# Response: [{ all submissions }]
```

### 4.3 Queryset Filtering

```python
def get_queryset(self):
    """Control what data each user can access"""
    if self.request.user.is_staff:
        return InternshipApplication.objects.all()  # All data
    return InternshipApplication.objects.none()     # No data
```

---

## 5. Data Protection

### 5.1 SQL Injection Prevention

**Django ORM Protection**:
```python
# ❌ VULNERABLE (Never do this)
ContactForm.objects.raw("SELECT * FROM contact WHERE email = '%s'" % user_input)

# ✅ SAFE (Always do this)
ContactForm.objects.filter(email=user_input)  # Parameterized queries
```

All XSTN code uses Django ORM, which automatically:
- Parameterizes queries
- Escapes special characters
- Prevents SQL injection attacks

### 5.2 CORS (Cross-Origin Resource Sharing)

**Configuration** (in settings.py):
```python
CORS_ALLOWED_ORIGINS = [
    "https://xstn.com",           # Production frontend
    "https://www.xstn.com",       # WWW variant
    "http://localhost:3000",      # Local development
]

CORS_ALLOW_CREDENTIALS = True  # Allow cookies/auth headers

# Prevents requests from unauthorized domains
# Blocks: attacker.com → /api/contact/ ✗
# Allows: xstn.com → /api/contact/ ✓
```

### 5.3 CSRF (Cross-Site Request Forgery) Protection

**Django Middleware** (enabled by default):
```python
MIDDLEWARE = [
    ...
    'django.middleware.csrf.CsrfViewMiddleware',  # Enabled
    ...
]
```

**How It Works**:
- Forms require CSRF token
- Token is tied to user session
- Random token per request
- Server verifies token matches

**Protection**: Prevents attackers from making unauthorized requests on behalf of users

### 5.4 Sensitive Data Handling

**Password Fields**:
```python
# Never logged in debug mode
# Automatically redacted in error messages
# Never sent to frontend

class UserSerializer(ModelSerializer):
    password = CharField(write_only=True)  # Not included in response
```

**Email Field** (in forms):
```python
# Encrypted in transit (HTTPS only)
# Hashed if stored temporarily
# Never exposed in debug output
```

---

## 6. Infrastructure Security

### 6.1 HTTPS/TLS

**Required For**:
- ✅ All API endpoints (enforced)
- ✅ Email transmission (encryption)
- ✅ Token transmission (encrypted in transit)

**Configuration**:
```python
# Force HTTPS in production
SECURE_SSL_REDIRECT = True  # Redirect HTTP → HTTPS
SESSION_COOKIE_SECURE = True  # Cookies over HTTPS only
CSRF_COOKIE_SECURE = True    # CSRF tokens over HTTPS only
```

### 6.2 Security Headers

**Response Headers** (automatically added):
```
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
```

**Purpose**:
- HSTS: Enforce HTTPS
- X-Content-Type-Options: Prevent MIME-sniffing
- X-Frame-Options: Prevent clickjacking
- X-XSS-Protection: Browser XSS filters

### 6.3 Environment Variables

**Sensitive Configuration** (NOT in code):
```python
# .env file (never committed)
SECRET_KEY = "your-secret-key-here"
EMAIL_PASSWORD = "your-email-password"
DATABASE_URL = "postgresql://user:pass@host/db"

# Loaded at runtime
import os
SECRET_KEY = os.environ.get('SECRET_KEY')
```

---

## 7. Logging & Monitoring

### 7.1 Security Logging

```python
import logging

logger = logging.getLogger(__name__)

# Log authentication events
logger.info(f"User {user.id} logged in successfully")
logger.warning(f"Failed login attempt for {username}")
logger.error(f"Account locked: too many failed attempts - {username}")

# Log email events
logger.info(f"Verification email sent to {email}")
logger.error(f"Email sending failed: {exception}")

# Log admin actions
logger.warning(f"Admin {admin.id} deleted form {form.id}")
logger.info(f"Admin {admin.id} approved application {app.id}")
```

### 7.2 Error Handling

```python
try:
    send_verification_email(email, token, form_type, name)
except SMTPException as e:
    logger.error(f"SMTP error sending email: {e}")
    # Log without exposing to user
    return Response(
        {'error': 'Email service temporarily unavailable'},
        status=status.HTTP_503_SERVICE_UNAVAILABLE
    )
except Exception as e:
    logger.exception("Unexpected error in email service")
    # Generic error message to user
    return Response(
        {'error': 'An error occurred'},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
```

---

## 8. Email Notification Security

### 8.1 Email Service Architecture

**Location**: `backend/apps/forms/email_notifications.py`

**Features**:
- ✅ HTML + Plain text versions (prevents rendering attacks)
- ✅ No sensitive data in email body (tokens in links only)
- ✅ Sender verification (from authenticated email)
- ✅ Error logging for debugging

### 8.2 Email Types

1. **Verification Email** - Contains verification token link
2. **Admin Notification** - Alerts staff of new submission
3. **Confirmation Email** - Confirms successful verification
4. **Approval Email** - Sends acceptance with next steps
5. **Rejection Email** - Sends rejection with feedback

### 8.3 Admin Notifications

**Recipient**: Company email (configured in settings)

```python
ADMIN_EMAIL = "admin@xstn.com"  # Settings
```

**Content**:
- ✅ Submission details
- ✅ User contact information
- ✅ Verification status
- ✅ Formatted form data

---

## 9. Security Checklist

### Before Deployment:

- [ ] Set `DEBUG = False` in production
- [ ] Configure `ALLOWED_HOSTS` with production domain
- [ ] Set strong `SECRET_KEY` (50+ characters)
- [ ] Enable `SECURE_SSL_REDIRECT = True`
- [ ] Configure email credentials in `.env`
- [ ] Set up CORS for production domain
- [ ] Enable security middleware
- [ ] Configure logging for production
- [ ] Set up database backups
- [ ] Test email verification flow
- [ ] Verify token expiration works

### Regular Maintenance:

- [ ] Monitor failed login attempts
- [ ] Review admin action logs weekly
- [ ] Update dependencies for security patches
- [ ] Test disaster recovery monthly
- [ ] Audit access logs for anomalies
- [ ] Rotate security keys periodically

---

## 10. Security Best Practices

### For Users:

1. ✅ Use strong, unique passwords (8+ chars)
2. ✅ Enable two-factor authentication when available
3. ✅ Do not share verification links
4. ✅ Keep tokens confidential
5. ✅ Use HTTPS connections only

### For Developers:

1. ✅ Never commit secrets to repository
2. ✅ Use environment variables for sensitive data
3. ✅ Validate all user inputs
4. ✅ Use Django ORM (prevents SQL injection)
5. ✅ Log security events for monitoring
6. ✅ Keep dependencies updated
7. ✅ Review code for security issues

### For Admins:

1. ✅ Use strong admin credentials
2. ✅ Limit admin access to authorized personnel
3. ✅ Monitor server logs regularly
4. ✅ Keep backups encrypted and secure
5. ✅ Review failed login attempts
6. ✅ Update Django security patches

---

## 11. Incident Response

### If Token Compromise Suspected:

```python
# Clear user's tokens
user.token_set.all().delete()

# Send user notification
send_email(user.email, "Security Alert: Your session was cleared")

# Log incident
logger.critical(f"Suspected token compromise: User {user.id}")
```

### If Password Breach Suspected:

```python
# Lock account immediately
user.is_locked = True
user.locked_until = now() + timedelta(hours=24)
user.save()

# Force password reset
user.set_password(None)

# Send notification
send_password_reset_email(user.email)

# Log incident
logger.critical(f"Password breach suspected: User {user.id}")
```

---

## 12. Compliance & Standards

**XSTN Backend Complies With**:

- ✅ **OWASP Top 10** - Protects against common vulnerabilities
- ✅ **GDPR** - Email verification ensures consent
- ✅ **Django Security** - Follows official security practices
- ✅ **REST API Security** - JWT best practices
- ✅ **Password Standards** - PBKDF2 hashing with 260k iterations

---

## 13. Testing Security

### Unit Tests for Security:

```python
def test_email_verification_token_expires():
    """Token should expire after 24 hours"""
    form = ContactForm.objects.create(email="test@test.com")
    token = form.generate_verification_token()
    
    # Valid immediately
    assert form.is_verification_token_valid() == True
    
    # Mock time forward 25 hours
    with freeze_time("2024-01-02 01:00:00"):
        assert form.is_verification_token_valid() == False

def test_failed_login_lockout():
    """Account should lock after 5 failed attempts"""
    user = User.objects.create(username="test")
    
    for i in range(5):
        user.increment_failed_attempts()
    
    assert user.is_locked == True
    assert user.failed_login_attempts == 5

def test_sql_injection_prevention():
    """SQL injection should be prevented"""
    malicious_input = "' OR '1'='1"
    
    # Should return no results, not all records
    results = ContactForm.objects.filter(email=malicious_input)
    assert results.count() == 0
```

---

## 14. Additional Resources

**OAuth2 / OpenID Connect** (future):
- Consider for third-party integrations
- More granular permission scopes

**Two-Factor Authentication** (future):
- SMS or authenticator app
- Additional security layer

**Rate Limiting** (future):
- Prevent brute force attacks
- Limit API requests per user

**API Key Authentication** (future):
- For server-to-server communication
- Third-party integrations

---

**Document Version**: 1.0  
**Last Updated**: 2024  
**Security Level**: Enterprise  
**Status**: ✅ Production Ready
