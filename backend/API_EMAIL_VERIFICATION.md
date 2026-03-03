# XSTN Forms API - Email Verification & Notifications

Complete API documentation with email verification workflow and admin notifications.

## Overview

The XSTN Forms API now includes:
- ✅ Form submission with automatic email verification
- ✅ Email verification token system (24-hour expiry)
- ✅ Admin notifications to company email
- ✅ User confirmation emails
- ✅ Application approval/rejection workflow

---

## Authentication

### Token-Based Authentication

All admin endpoints require authentication:

```bash
# Get Token
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"password"}'

Response:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}

# Use Access Token
curl -X GET http://localhost:8000/api/contact/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."

# Refresh Token When Expired
curl -X POST http://localhost:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh":"..."}'
```

---

## Form Submission & Email Verification Workflow

### User Journey:

```
User fills form → Submit → Verification email sent → 
User clicks link → Email verified → Admin notified → 
Admin dashboard updated
```

---

## 1. CONTACT FORM

### 1.1 Submit Contact Form

**Endpoint**: `POST /api/contact/`

**Permission**: AllowAny (Public)

**Request**:
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "subject": "Business Inquiry",
  "message": "I would like to discuss a partnership opportunity."
}
```

**Response (201 Created)**:
```json
{
  "message": "✓ Form submitted! Please verify your email to complete the process.",
  "data": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "subject": "Business Inquiry",
    "message": "I would like to discuss a partnership...",
    "is_verified": false,
    "created_at": "2024-01-15T10:30:00Z"
  },
  "next_step": "Check your email for verification link (valid for 24 hours)"
}
```

**What Happens**:
- ✅ Form stored in database with `is_verified: false`
- ✅ Unique verification token generated
- ✅ Verification email sent to user with 24-hour link
- ✅ Admin NOT notified yet (waits for verification)

### 1.2 Verify Contact Form Email

**Endpoint**: `POST /api/contact/verify_email/`

**Permission**: AllowAny (Public)

**Request**:
```json
{
  "token": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"
}
```

**Response (200 OK)**:
```json
{
  "message": "✓ Email verified successfully! We have received your submission.",
  "verified": true
}
```

**What Happens**:
- ✅ Token validated (must be within 24 hours)
- ✅ Form marked as `is_verified: true`
- ✅ Verification timestamp recorded
- ✅ Admin notification email sent to company email
- ✅ Confirmation email sent to user
- ✅ Token cleared from database

**Email Sent to Admin**:
```
To: admin@xstn.com
Subject: 📨 Contact Form Received: Business Inquiry

New contact form submission received:

Name: John Doe
Email: john@example.com
Phone: +1234567890
Subject: Business Inquiry

Message:
I would like to discuss a partnership opportunity.

---
Status: ✓ Email Verified
Submission Date: 2024-01-15 10:35 AM
```

**Email Sent to User**:
```
To: john@example.com
Subject: XSTN - We received your message

Hello John,

Thank you for contacting XSTN. Your email has been verified and we have received your submission. Our team will review it and get back to you shortly.

Best regards,
XSTN Team
```

### 1.3 View All Contact Forms (Admin Only)

**Endpoint**: `GET /api/contact/`

**Permission**: IsStaff (Admin only)

**Request**:
```bash
curl -X GET http://localhost:8000/api/contact/ \
  -H "Authorization: Bearer <admin_token>"
```

**Response (200 OK)**:
```json
[
  {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "subject": "Business Inquiry",
    "message": "I would like to discuss...",
    "is_verified": true,
    "verified_at": "2024-01-15T10:35:00Z",
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

---

## 2. INQUIRY FORM

### 2.1 Submit Inquiry

**Endpoint**: `POST /api/inquiry/`

**Permission**: AllowAny

**Request**:
```json
{
  "name": "Jane Smith",
  "email": "jane@company.com",
  "company": "ABC Corp",
  "project_type": "Web Application",
  "budget_range": "50000-100000",
  "timeline": "3-6 months",
  "message": "We need a custom web app for our business."
}
```

**Response (201 Created)**:
```json
{
  "message": "✓ Inquiry received! Please verify your email.",
  "data": { ... },
  "next_step": "Check your email for verification link"
}
```

### 2.2 Verify Inquiry Email

**Endpoint**: `POST /api/inquiry/verify_email/`

**Request**:
```json
{
  "token": "verification_token_here"
}
```

---

## 3. INTERNSHIP APPLICATION

### 3.1 Submit Application

**Endpoint**: `POST /api/internship/`

**Request**:
```json
{
  "full_name": "Alex Johnson",
  "email": "alex@student.com",
  "phone": "+1234567890",
  "university": "MIT",
  "major": "Computer Science",
  "year": "Junior",
  "skills": "Python, JavaScript, React",
  "portfolio_url": "https://github.com/alex",
  "cover_letter": "I am interested in..."
}
```

**Response (201 Created)**:
```json
{
  "message": "✓ Application submitted! Please verify your email.",
  "data": { ... }
}
```

### 3.2 Verify Application Email

**Endpoint**: `POST /api/internship/verify_email/`

**Request**:
```json
{
  "token": "verification_token_here"
}
```

### 3.3 Admin Approve Application

**Endpoint**: `POST /api/internship/{id}/approve/`

**Permission**: IsAuthenticated + Staff

**Request**:
```json
{
  "next_steps": "Please join our orientation on Monday at 10 AM."
}
```

**Response**:
```json
{
  "message": "✓ Applicant approved and email sent."
}
```

**Email Sent to Applicant**:
```
To: alex@student.com
Subject: XSTN - Congratulations! You're Selected

Dear Alex,

Congratulations! We are excited to inform you that your internship application has been approved.

Next Steps:
Please join our orientation on Monday at 10 AM.

We look forward to working with you!

Best regards,
XSTN Team
```

### 3.4 Admin Reject Application

**Endpoint**: `POST /api/internship/{id}/reject/`

**Permission**: IsAuthenticated + Staff

**Request**:
```json
{
  "reason": "We received many qualified applications and selected other candidates."
}
```

**Response**:
```json
{
  "message": "✓ Applicant notified."
}
```

**Email Sent to Applicant**:
```
To: alex@student.com
Subject: XSTN - Application Status Update

Dear Alex,

Thank you for applying to XSTN's internship program.

Status: Not Selected

Reason: We received many qualified applications and selected other candidates.

We appreciate your interest and encourage you to apply again in the future.

Best regards,
XSTN Team
```

---

## 4. DEVELOPER APPLICATION

### 4.1 Submit Application

**Endpoint**: `POST /api/developer/`

**Request**:
```json
{
  "full_name": "Sarah Developer",
  "email": "sarah.dev@gmail.com",
  "phone": "+1234567890",
  "role_interested": "Full Stack Developer",
  "experience_level": "3+ years",
  "skills": "React, Node.js, PostgreSQL",
  "github_url": "https://github.com/sarah",
  "portfolio_url": "https://sarahdev.com",
  "why_join": "I love innovative projects..."
}
```

### 4.2 Verify Email

**Endpoint**: `POST /api/developer/verify_email/`

### 4.3 Admin Approve/Reject

Similar to internship (see section 3.3 & 3.4)

---

## 5. JOIN APPLICATION

### 5.1 Submit Application

**Endpoint**: `POST /api/join/`

**Request**:
```json
{
  "full_name": "Mark Entrepreneur",
  "email": "mark@startup.com",
  "role_interested": "Co-Founder",
  "why_join": "I believe in XSTN's mission..."
}
```

### 5.2 Verify Email

**Endpoint**: `POST /api/join/verify_email/`

---

## 6. CONSULTATION REQUEST

### 6.1 Submit Request

**Endpoint**: `POST /api/consultation/`

**Request**:
```json
{
  "full_name": "Dr. Smith",
  "email": "dr.smith@hospital.com",
  "phone": "+1234567890",
  "consultation_type": "Technical Strategy",
  "preferred_date": "2024-02-15",
  "requirement": "Need advice on digital transformation..."
}
```

### 6.2 Verify Email

**Endpoint**: `POST /api/consultation/verify_email/`

---

## 7. NEWSLETTER SUBSCRIPTION

### 7.1 Subscribe

**Endpoint**: `POST /api/newsletter/`

**Request**:
```json
{
  "email": "subscriber@example.com"
}
```

**Response (201 Created)**:
```json
{
  "message": "✓ Successfully subscribed to newsletter!",
  "data": { ... }
}
```

**Email Sent**:
```
To: subscriber@example.com
Subject: XSTN - Welcome to Our Newsletter

Thank you for subscribing to XSTN's newsletter!

You will now receive updates about:
- Latest projects and innovations
- Internship and career opportunities
- Tech insights and industry news

Best regards,
XSTN Team
```

### 7.2 Unsubscribe

**Endpoint**: `POST /api/newsletter/{id}/unsubscribe/`

**Permission**: AllowAny

**Response**:
```json
{
  "message": "✓ Unsubscribed successfully"
}
```

---

## 8. TESTIMONIAL

### 8.1 Submit Testimonial

**Endpoint**: `POST /api/testimonial/`

**Request**:
```json
{
  "name": "Happy Client",
  "email": "client@company.com",
  "company": "Tech Corp",
  "rating": 5,
  "testimonial": "XSTN's work exceeded our expectations!",
  "allow_display": true
}
```

**Response (201 Created)**:
```json
{
  "message": "✓ Testimonial submitted! Check your email to verify.",
  "data": { ... },
  "note": "Testimonials appear after admin approval"
}
```

### 8.2 Verify Email

**Endpoint**: `POST /api/testimonial/verify_email/`

**Request**:
```json
{
  "token": "verification_token_here"
}
```

**Response**:
```json
{
  "message": "✓ Email verified! Awaiting admin approval.",
  "verified": true
}
```

---

## Email Verification System Details

### Token Format

- **Type**: UUID4 hex string
- **Length**: 32 characters
- **Format**: `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6`
- **Generation**: Random, cryptographically secure

### Token Lifecycle

```
1. Form submitted
   ↓
2. Token generated & stored in database
   ↓
3. Email sent with verification link
   ↓
4. User clicks link (24 hours available)
   ↓
5. Token validated in API
   ↓
6. Email marked verified
   ↓
7. Token cleared from database
```

### Token Expiration

- **Valid For**: 24 hours from creation
- **After Expiration**: "Verification token has expired. Please submit the form again."
- **New Token**: Generate list as needed

---

## Error Responses

### Invalid Token

**Status**: 400 Bad Request

```json
{
  "error": "Invalid or expired verification token"
}
```

### Token Not Provided

**Status**: 400 Bad Request

```json
{
  "error": "Verification token is required"
}
```

### Token Expired

**Status**: 400 Bad Request

```json
{
  "error": "Verification token has expired. Please submit the form again."
}
```

### Duplicate Email (Newsletter)

**Status**: 400 Bad Request

```json
{
  "message": "Email already subscribed to newsletter"
}
```

### Unauthorized (Admin Only)

**Status**: 401 Unauthorized

```json
{
  "detail": "Authentication credentials were not provided."
}
```

### Forbidden (Non-Staff)

**Status**: 403 Forbidden

```json
{
  "detail": "You do not have permission to perform this action."
}
```

---

## Complete Workflow Examples

### Example 1: Contact Form with Verification

```bash
# Step 1: User submits form
curl -X POST http://localhost:8000/api/contact/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John",
    "email": "john@example.com",
    "phone": "123456",
    "subject": "Hello",
    "message": "Test message"
  }'

# Response: Contains next_step instruction
# Email sent to john@example.com with verification link

# Step 2: User clicks email link (simulating with token)
curl -X POST http://localhost:8000/api/contact/verify_email/ \
  -H "Content-Type: application/json" \
  -d '{"token":"<token_from_email>"}'

# Response: Email verified
# Admin notification sent
# Confirmation email sent to user
```

### Example 2: Application Approval Workflow

```bash
# Step 1: Candidate submits internship application
curl -X POST http://localhost:8000/api/internship/ \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Alex",
    "email": "alex@student.com",
    ...
  }'

# Step 2: Candidate verifies email
curl -X POST http://localhost:8000/api/internship/verify_email/ \
  -H "Content-Type: application/json" \
  -d '{"token":"<token>"}'

# Step 3: Admin approves application
curl -X POST http://localhost:8000/api/internship/1/approve/ \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{"next_steps": "Join orientation on Monday"}'

# Approval email sent to alex@student.com
```

---

## Admin Dashboard Features

### View All Submissions

Only verified submissions are counted in admin dashboard:

```python
# Get all verified contact forms
verified_forms = ContactForm.objects.filter(is_verified=True)

# Get all unverified (pending verification)
pending_forms = ContactForm.objects.filter(is_verified=False)

# Get with verification status
forms_with_status = ContactForm.objects.all().values('id', 'is_verified', 'verified_at')
```

---

## Status Codes Reference

| Code | Meaning | Usage |
|------|---------|-------|
| 200 | OK | Email verified successfully |
| 201 | Created | Form submitted successfully |
| 400 | Bad Request | Invalid token, missing fields |
| 401 | Unauthorized | Missing authentication token |
| 403 | Forbidden | Insufficient permissions (admin only) |
| 404 | Not Found | Token or form doesn't exist |
| 500 | Server Error | Email service failure |

---

## Rate Limiting (Future Enhancement)

When implemented, these limits will apply:

```
- Form submission: 5 forms per hour per IP
- Verification attempt: 10 attempts per token
- Email: 100 emails per hour
- Admin actions: Unlimited (staff only)
```

---

## Security Notes

- ✅ All tokens expire after 24 hours
- ✅ Tokens are stored securely in database
- ✅ Tokens are one-time use (cleared after verification)
- ✅ Email addresses are validated with regex
- ✅ All API endpoints use HTTPS in production
- ✅ Admin actions require authentication
- ✅ User data is never exposed in error messages

---

**API Version**: 1.0  
**Updated**: 2024  
**Status**: ✅ Production Ready  
**Base URL**: `https://xstn.com/api/`
