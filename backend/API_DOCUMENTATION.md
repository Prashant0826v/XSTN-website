# XSTN Backend - Complete API Documentation

## Overview
This document provides comprehensive documentation for all XSTN backend API endpoints. The backend is built with **Django** and **Django REST Framework**.

## Base URL
```
http://localhost:8000/api/
```

## Authentication
- **Default Authentication**: AllowAny (for form submissions)
- **Admin Operations**: Requires admin user or staff permission
- **Token-Based**: JWT tokens available at `/api/token/`

---

## API Endpoints

### 1. Contact Forms
**Base URL**: `/api/forms/contact-forms/`

#### Create Contact Form (POST)
```http
POST /api/forms/contact-forms/
Content-Type: application/json

{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "subject": "Website Inquiry",
    "message": "I would like to know more about your services."
}
```

**Response (201 Created)**:
```json
{
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "subject": "Website Inquiry",
    "message": "I would like to know more about your services.",
    "is_read": false,
    "created_at": "2024-01-15T10:30:00Z"
}
```

#### List Contact Forms (GET)
```http
GET /api/forms/contact-forms/
```
*Admin only - Returns all contact forms*

#### Retrieve Contact Form (GET)
```http
GET /api/forms/contact-forms/{id}/
```

#### Update Contact Form (PATCH)
```http
PATCH /api/forms/contact-forms/{id}/
Content-Type: application/json

{
    "is_read": true
}
```

#### Delete Contact Form (DELETE)
```http
DELETE /api/forms/contact-forms/{id}/
```

---

### 2. Inquiry Forms
**Base URL**: `/api/forms/inquiry-forms/`

#### Create Inquiry Form (POST)
```http
POST /api/forms/inquiry-forms/
Content-Type: application/json

{
    "name": "Jane Smith",
    "email": "jane@company.com",
    "company": "Tech Corp",
    "project_type": "E-Commerce Platform",
    "budget_range": "$10,000 - $50,000",
    "timeline": "3-6 months",
    "message": "We need a custom e-commerce platform with advanced features."
}
```

**Response (201 Created)**:
```json
{
    "id": 1,
    "name": "Jane Smith",
    "email": "jane@company.com",
    "company": "Tech Corp",
    "project_type": "E-Commerce Platform",
    "budget_range": "$10,000 - $50,000",
    "timeline": "3-6 months",
    "message": "We need a custom e-commerce platform with advanced features.",
    "is_read": false,
    "created_at": "2024-01-15T11:00:00Z"
}
```

#### List Inquiry Forms (GET)
```http
GET /api/forms/inquiry-forms/
```
*Admin only - Returns all inquiry forms*

---

### 3. Internship Applications
**Base URL**: `/api/forms/internship-applications/`

#### Create Internship Application (POST)
```http
POST /api/forms/internship-applications/
Content-Type: application/json

{
    "full_name": "Alex Johnson",
    "email": "alex@student.edu",
    "phone": "+1987654321",
    "university": "MIT",
    "skills": "Python, JavaScript, React",
    "experience": "1 year of freelance web development",
    "portfolio_url": "https://alexportfolio.com",
    "resume_url": "https://drive.google.com/resume"
}
```

**Response (201 Created)**:
```json
{
    "id": 1,
    "full_name": "Alex Johnson",
    "email": "alex@student.edu",
    "phone": "+1987654321",
    "university": "MIT",
    "skills": "Python, JavaScript, React",
    "experience": "1 year of freelance web development",
    "portfolio_url": "https://alexportfolio.com",
    "resume_url": "https://drive.google.com/resume",
    "status": "pending",
    "notes": "",
    "is_read": false,
    "created_at": "2024-01-15T12:00:00Z"
}
```

#### Status Values
- `pending`: Application received, awaiting review
- `reviewed`: Application has been reviewed
- `selected`: Applicant selected for internship
- `rejected`: Application rejected

#### List Applications (GET)
```http
GET /api/forms/internship-applications/
```
*Admin only*

#### Update Status (PATCH)
```http
PATCH /api/forms/internship-applications/{id}/
Content-Type: application/json

{
    "status": "selected",
    "notes": "Excellent candidate, strong portfolio"
}
```

---

### 4. Developer Applications
**Base URL**: `/api/forms/developer-applications/`

#### Create Developer Application (POST)
```http
POST /api/forms/developer-applications/
Content-Type: application/json

{
    "full_name": "Sarah Chen",
    "email": "sarah@dev.com",
    "phone": "+1555555555",
    "role_interested": "Full Stack Developer",
    "experience_level": "intermediate",
    "skills": "Node.js, React, MongoDB, PostgreSQL",
    "portfolio_url": "https://sarahdev.com",
    "github_url": "https://github.com/sarahchen",
    "message": "Excited to join XSTN and contribute to innovative tech projects."
}
```

**Response (201 Created)**:
```json
{
    "id": 1,
    "full_name": "Sarah Chen",
    "email": "sarah@dev.com",
    "phone": "+1555555555",
    "role_interested": "Full Stack Developer",
    "experience_level": "intermediate",
    "skills": "Node.js, React, MongoDB, PostgreSQL",
    "portfolio_url": "https://sarahdev.com",
    "github_url": "https://github.com/sarahchen",
    "message": "Excited to join XSTN and contribute to innovative tech projects.",
    "status": "pending",
    "is_read": false,
    "created_at": "2024-01-15T13:00:00Z"
}
```

#### Experience Levels
- `beginner`: Less than 1 year
- `intermediate`: 1-3 years
- `advanced`: 3-5 years
- `expert`: 5+ years

---

### 5. Join Applications
**Base URL**: `/api/forms/join-applications/`

#### Create Join Application (POST)
```http
POST /api/forms/join-applications/
Content-Type: application/json

{
    "full_name": "Michael Brown",
    "email": "michael@email.com",
    "role_interested": "Project Manager",
    "why_join": "I believe in XSTN's mission to empower tech students across 30+ colleges and 8 tech domains."
}
```

**Response (201 Created)**:
```json
{
    "id": 1,
    "full_name": "Michael Brown",
    "email": "michael@email.com",
    "role_interested": "Project Manager",
    "why_join": "I believe in XSTN's mission to empower tech students across 30+ colleges and 8 tech domains.",
    "status": "pending",
    "is_read": false,
    "created_at": "2024-01-15T14:00:00Z"
}
```

#### Status Values
- `pending`: Application received
- `reviewed`: Application reviewed
- `accepted`: Application accepted
- `rejected`: Application rejected

---

### 6. Consultation Requests
**Base URL**: `/api/forms/consultation-requests/`

#### Create Consultation Request (POST)
```http
POST /api/forms/consultation-requests/
Content-Type: application/json

{
    "full_name": "Emily Wilson",
    "email": "emily@company.com",
    "phone": "+1777777777",
    "consultation_type": "website",
    "preferred_date": "2024-02-01",
    "requirement": "We need a modern, responsive website for our startup with SEO optimization."
}
```

**Response (201 Created)**:
```json
{
    "id": 1,
    "full_name": "Emily Wilson",
    "email": "emily@company.com",
    "phone": "+1777777777",
    "consultation_type": "website",
    "preferred_date": "2024-02-01",
    "requirement": "We need a modern, responsive website for our startup with SEO optimization.",
    "status": "pending",
    "is_read": false,
    "created_at": "2024-01-15T15:00:00Z"
}
```

#### Consultation Types
- `website`: Website development consultation
- `app`: Mobile app development consultation
- `ui_ux`: UI/UX design consultation
- `business`: Business strategy consultation
- `other`: Other consultation types

#### Status Values
- `pending`: Request received, awaiting scheduling
- `scheduled`: Consultation scheduled
- `completed`: Consultation completed
- `cancelled`: Consultation cancelled

---

### 7. Newsletter Subscriptions
**Base URL**: `/api/forms/newsletter-subscriptions/`

#### Create Newsletter Subscription (POST)
```http
POST /api/forms/newsletter-subscriptions/
Content-Type: application/json

{
    "email": "subscriber@example.com"
}
```

**Response (201 Created)**:
```json
{
    "message": "Successfully subscribed to newsletter",
    "data": {
        "id": 1,
        "email": "subscriber@example.com",
        "is_active": true,
        "created_at": "2024-01-15T16:00:00Z"
    }
}
```

#### Error Response (Duplicate Subscription)
```json
{
    "message": "Email already subscribed to newsletter"
}
```
*Status: 400 Bad Request*

#### Unsubscribe (POST)
```http
POST /api/forms/newsletter-subscriptions/{id}/unsubscribe/
Authorization: Bearer {token}
```

**Response (200 OK)**:
```json
{
    "message": "Successfully unsubscribed from newsletter"
}
```

#### List Subscriptions (GET)
```http
GET /api/forms/newsletter-subscriptions/
```
*Admin only*

---

### 8. Testimonials
**Base URL**: `/api/forms/testimonials/`

#### Create Testimonial (POST)
```http
POST /api/forms/testimonials/
Content-Type: application/json

{
    "name": "Robert Davis",
    "company": "Tech Innovations Inc",
    "email": "robert@techinnovations.com",
    "rating": 5,
    "message": "XSTN has been instrumental in helping us build an amazing tech team. Their network and resources are invaluable!"
}
```

**Response (201 Created)**:
```json
{
    "message": "Thank you for your testimonial! It will be reviewed and published shortly.",
    "data": {
        "id": 1,
        "name": "Robert Davis",
        "company": "Tech Innovations Inc",
        "email": "robert@techinnovations.com",
        "rating": 5,
        "message": "XSTN has been instrumental in helping us build an amazing tech team. Their network and resources are invaluable!",
        "is_approved": false,
        "created_at": "2024-01-15T17:00:00Z"
    }
}
```

#### List Approved Testimonials (GET)
```http
GET /api/forms/testimonials/
```
**Response**: Only approved testimonials are returned

#### Rating Values
- `1` to `5` (1-5 star rating)

#### Admin: List All Testimonials
```http
GET /api/forms/testimonials/
Authorization: Bearer {admin_token}
```
*Admin users see all testimonials (approved and pending)*

---

## Form Submission Email Notifications

### Email Recipients

#### 1. Contact Form
- **Admin**: Receives notification of new contact
- **User**: Receives confirmation that message was received

#### 2. Inquiry Form
- **Admin**: Receives detailed inquiry information
- **User**: Receives confirmation that proposal request was made

#### 3. Internship Application
- **Admin**: Receives application details
- **User**: Receives confirmation of application submission

#### 4. Developer Application
- **Admin**: Receives application with links to portfolio and GitHub
- **User**: Receives confirmation and timeline for review

#### 5. Join Application
- **Admin**: Receives application details
- **User**: Receives confirmation and expected review timeline

#### 6. Consultation Request
- **Admin**: Receives consultation details and preferred date
- **User**: Receives confirmation that specialist will contact within 24 hours

#### 7. Newsletter Subscription
- **User**: Receives welcome email confirming subscription

#### 8. Testimonial
- **User**: Receives confirmation that testimonial will be reviewed

### Email Configuration
All emails are configured using Django's email backend. Ensure the following settings are configured in `settings.py`:

```python
# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'noreply@xstn.com'
```

---

## Admin Dashboard Features

### Contact Forms Admin
- View all submissions
- Mark as read/unread
- Search by name, email, subject
- Filter by status and date

### Internship Applications Admin
- View applications with full details
- Change status (pending → reviewed → selected/rejected)
- Add review notes
- Bulk actions (mark as read, change status)

### Developer Applications Admin
- Full application management
- View portfolio and GitHub links
- Track experience level distribution
- Bulk status updates

### Newsletter Subscriptions Admin
- Manage subscriber list
- Activate/deactivate subscriptions
- Export subscriber emails
- View subscription date

### Testimonials Admin
- Review pending testimonials
- Approve/reject testimonials
- View rating distribution
- Featured testimonials management

---

## HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 400 | Bad Request - Invalid data |
| 404 | Not Found - Resource not found |
| 500 | Server Error - Internal server error |

---

## Error Response Format

All error responses follow this format:

```json
{
    "error": "Error message",
    "details": {
        "field_name": ["Specific error message"]
    }
}
```

Example:
```json
{
    "error": "Validation error",
    "details": {
        "email": ["Invalid email format"],
        "name": ["This field is required"]
    }
}
```

---

## Rate Limiting

- No rate limiting is currently enforced
- Implement in production for security

---

## CORS Configuration

Current CORS settings allow requests from:
- Local development (localhost:3000)
- Production domains (configured in settings.py)

---

## Testing the API

### Using cURL

#### Create Contact Form
```bash
curl -X POST http://localhost:8000/api/forms/contact-forms/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "phone": "+1234567890",
    "subject": "Test Subject",
    "message": "Test message"
  }'
```

#### Get Testimonials
```bash
curl -X GET http://localhost:8000/api/forms/testimonials/
```

### Using Python Requests

```python
import requests

# Create contact form
data = {
    'name': 'John Doe',
    'email': 'john@example.com',
    'phone': '+1234567890',
    'subject': 'Inquiry',
    'message': 'Hello, I have a question.'
}

response = requests.post(
    'http://localhost:8000/api/forms/contact-forms/',
    json=data
)
print(response.json())
```

### Using Postman

1. Create a new collection "XSTN API"
2. Import this documentation or manually create requests
3. Test each endpoint
4. Use the environments feature to manage base URL

---

## API Endpoints Summary

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/forms/contact-forms/` | Create contact form |
| GET | `/api/forms/contact-forms/` | List contact forms (admin) |
| POST | `/api/forms/inquiry-forms/` | Create inquiry |
| GET | `/api/forms/inquiry-forms/` | List inquiries (admin) |
| POST | `/api/forms/internship-applications/` | Apply for internship |
| GET | `/api/forms/internship-applications/` | List applications (admin) |
| POST | `/api/forms/developer-applications/` | Apply as developer |
| GET | `/api/forms/developer-applications/` | List applications (admin) |
| POST | `/api/forms/join-applications/` | Apply to join |
| GET | `/api/forms/join-applications/` | List applications (admin) |
| POST | `/api/forms/consultation-requests/` | Request consultation |
| GET | `/api/forms/consultation-requests/` | List requests (admin) |
| POST | `/api/forms/newsletter-subscriptions/` | Subscribe to newsletter |
| GET | `/api/forms/newsletter-subscriptions/` | List subscriptions (admin) |
| POST | `/api/forms/testimonials/` | Submit testimonial |
| GET | `/api/forms/testimonials/` | Get testimonials |

---

## Future Enhancements

- [ ] Advanced filtering and pagination
- [ ] Webhook support for external integrations
- [ ] Rate limiting and throttling
- [ ] API versioning
- [ ] GraphQL endpoint
- [ ] OpenAPI/Swagger documentation
- [ ] Email template customization
- [ ] Multi-language support
