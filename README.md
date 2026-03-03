# XSTN - Student Tech Network: Complete Project Guide

## 🎯 Project Overview

XSTN (Student Tech Network) is a comprehensive platform designed to empower students across **30+ colleges** and **8 tech domains** to collaborate, learn, and innovate together. The project includes a modern frontend, robust Django backend, and extensive API integration.

---

## 📁 Project Structure

```
XSTN Project/
├── frontend/                          # Web application frontend
│   ├── index.html                     # Homepage
│   ├── about.html                     # About page
│   ├── services.html                  # Services page
│   ├── contact.html                   # Contact form
│   ├── consultation.html              # Consultation booking
│   ├── internship.html                # Internship applications
│   ├── join-developer.html            # Developer join form
│   ├── join.html                      # General join form
│   ├── partner.html                   # Partner page
│   ├── pricing.html                   # Pricing information
│   ├── projects.html                  # Projects showcase
│   ├── proposal.html                  # Proposal request
│   ├── api-client.js                  # **(NEW) API client library**
│   ├── auth.js                        # Authentication handler
│   ├── config.js                      # Configuration
│   ├── form.js                        # Form handling
│   ├── join.js                        # Join form logic
│   ├── style.css                      # Styling
│   ├── utils.js                       # Utility functions
│   ├── API_INTEGRATION.md             # **(NEW) Frontend integration guide**
│   ├── README.md                      # Frontend documentation
│   ├── assets/                        # Assets folder
│   │   ├── icons/                     # Icon files
│   │   └── images/                    # image files
│   └── runtime-config.js              # Runtime configuration
│
└── backend/                           # Django REST API backend
    ├── manage.py                      # Django management script
    ├── db.sqlite3                     # SQLite database
    ├── requirements.txt               # Python dependencies
    ├── API_DOCUMENTATION.md           # **(NEW) Complete API docs**
    ├── BACKEND_SETUP.md               # **(NEW) Setup & deployment guide**
    ├── README.md                      # Backend documentation
    ├── create_superuser.py            # Superuser creation script
    ├── test_email_config.py           # Email configuration test
    ├── verify_email.py                # Email verification
    │
    ├── config/                        # Django configuration
    │   ├── settings.py                # Django settings
    │   ├── urls.py                    # Main URL routing
    │   ├── wsgi.py                    # WSGI config
    │   └── asgi.py                    # ASGI config
    │
    ├── apps/
    │   ├── users/                     # User management app
    │   │   ├── models.py              # User model
    │   │   ├── views.py               # User viewsets
    │   │   ├── serializers.py         # User serializers
    │   │   ├── admin.py               # Admin registration
    │   │   └── migrations/            # Database migrations
    │   │
    │   └── forms/                     # Forms/submissions app
    │       ├── models.py              # **(UPDATED)** 8 form models
    │       ├── serializers.py         # **(UPDATED)** 8 serializers
    │       ├── views.py               # **(UPDATED)** 8 viewsets
    │       ├── admin.py               # **(UPDATED)** Admin configs
    │       ├── urls.py                # **(NEW)** Form URLs
    │       ├── migrations/            # Database migrations
    │       └── __init__.py
    │
    └── tests/                         # Test suite
        ├── test_user_model.py         # User model tests (11 tests)
        ├── test_form_models.py        # Form model tests (20 tests)
        ├── test_serializers.py        # Serializer tests (15 tests)
        ├── test_api_views.py          # API view tests (18 tests)
        ├── README.md                  # Testing documentation
        └── __pycache__/
```

---

## 🚀 Quick Start

### Frontend Setup

1. **Navigate to frontend directory**:
```bash
cd frontend
```

2. **Open in browser**:
   - Simply open any HTML file in your browser
   - No build process required for vanilla HTML/CSS/JS
   - Make sure backend is running for form submissions

### Backend Setup

1. **Navigate to backend directory**:
```bash
cd backend
```

2. **Create virtual environment**:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Create `.env` file** (see [Backend Setup Guide](./backend/BACKEND_SETUP.md)):
```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_ENGINE=django.db.backends.sqlite3
DATABASE_NAME=db.sqlite3
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

5. **Run migrations**:
```bash
python manage.py migrate
python manage.py createsuperuser
```

6. **Start server**:
```bash
python manage.py runserver
```

Server runs at: `http://localhost:8000`
Admin panel: `http://localhost:8000/admin/`

---

## 📋 Features Implemented

### ✅ Frontend Features
- **Modern Authentication System**: Login/Signup pages with password strength indicators
- **Responsive Design**: Works on desktop, tablet, and mobile
- **10 Main Pages**: Home, About, Services, Projects, Partner, Contact, Consultation, Join, Internship, Pricing, Proposal
- **8 Forms**: Contact, Inquiry, Internship, Developer, Join, Consultation, Newsletter, Testimonial
- **Dark Theme**: Professional dark mode with cyan and purple accents
- **Gradient Effects**: Modern UI with backdrop filters and smooth transitions
- **Navbar Integration**: Login/Signup buttons on all pages

### ✅ Backend Features
- **8 Form Models**: Complete data models for all frontend forms
- **RESTful API**: All CRUD operations with Django REST Framework
- **Email Notifications**: Auto-send emails for form submissions
- **Admin Dashboard**: Full admin interface for managing submissions
- **User Authentication**: JWT token-based authentication system
- **Comprehensive Tests**: 64+ test cases covering all models and API endpoints
- **Email Service**: Gmail SMTP integration for sending confirmations

### ✅ API Endpoints
- **Contact Forms**: `/api/forms/contact-forms/`
- **Inquiry Forms**: `/api/forms/inquiry-forms/`
- **Internship Applications**: `/api/forms/internship-applications/`
- **Developer Applications**: `/api/forms/developer-applications/`
- **Join Applications**: `/api/forms/join-applications/`
- **Consultation Requests**: `/api/forms/consultation-requests/`
- **Newsletter Subscriptions**: `/api/forms/newsletter-subscriptions/`
- **Testimonials**: `/api/forms/testimonials/`

---

## 🔗 Frontend-Backend Integration

### Step 1: Import API Client

In any form HTML file:
```html
<script type="module">
    import { submitContactForm, showSuccessMessage, showErrorMessage } from './api-client.js';
    
    document.getElementById('contactForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const result = await submitContactForm({
            name: document.getElementById('name').value,
            email: document.getElementById('email').value,
            phone: document.getElementById('phone').value,
            subject: document.getElementById('subject').value,
            message: document.getElementById('message').value
        });
        
        if (result.success) {
            showSuccessMessage('✓ Your message has been sent!');
            document.getElementById('contactForm').reset();
        } else {
            showErrorMessage('✗ Error: ' + result.error);
        }
    });
</script>
```

### Step 2: Test Integration

See [API Integration Guide](./frontend/API_INTEGRATION.md) for detailed examples.

---

## 📚 Documentation

### Frontend Documentation
- [Frontend README](./frontend/README.md)
- **[NEW] API Integration Guide](./frontend/API_INTEGRATION.md)** - How to connect forms to backend
- [API Client Reference](./frontend/api-client.js) - All available functions

### Backend Documentation
- [Backend README](./backend/README.md)
- **[NEW] Backend Setup Guide](./backend/BACKEND_SETUP.md)** - Installation and deployment
- **[NEW] API Documentation](./backend/API_DOCUMENTATION.md)** - Complete API reference
- [Testing Documentation](./backend/tests/README.md) - Test cases and running tests
- [Email Setup](./backend/EMAIL_SETUP.md)
- [Django Setup](./backend/DJANGO_SETUP.md)

---

## 🧪 Testing

### Run All Tests
```bash
cd backend
python manage.py test
```

### Run Specific Test Module
```bash
python manage.py test tests.test_form_models
python manage.py test tests.test_api_views
```

### Test Coverage
- **User Model**: 11 tests
- **Form Models**: 20 tests (5 tests per model × 4 models)
- **Serializers**: 15 tests
- **API Views**: 18 tests
- **Total**: 64+ tests

See [Testing Documentation](./backend/tests/README.md) for details.

---

## 📧 Email Configuration

### Gmail Setup
1. Enable 2-Step Verification on Google Account
2. Create an App Password (16 characters)
3. Add to `.env`:
```env
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Test Email
```bash
python backend/test_email_config.py
```

See [Email Setup Guide](./backend/EMAIL_SETUP.md) for more details.

---

## 🌐 API Reference Summary

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/forms/contact-forms/` | POST | Submit contact form |
| `/api/forms/inquiry-forms/` | POST | Submit inquiry/proposal |
| `/api/forms/internship-applications/` | POST | Apply for internship |
| `/api/forms/developer-applications/` | POST | Apply as developer |
| `/api/forms/join-applications/` | POST | Apply to join XSTN |
| `/api/forms/consultation-requests/` | POST | Request consultation |
| `/api/forms/newsletter-subscriptions/` | POST | Subscribe to newsletter |
| `/api/forms/testimonials/` | POST | Submit testimonial |

Full API documentation: [API_DOCUMENTATION.md](./backend/API_DOCUMENTATION.md)

---

## 🛠️ Technology Stack

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with gradients and animations
- **Vanilla JavaScript**: No framework dependencies
- **ES6 Modules**: Organized code structure

### Backend
- **Python 3.8+**: Programming language
- **Django 3.2+**: Web framework
- **Django REST Framework**: API development
- **PostgreSQL/SQLite**: Database
- **JWT**: Token-based authentication
- **Django Cors**: Cross-origin support

### DevOps
- **Git**: Version control
- **Docker**: Containerization (optional)
- **Heroku**: Cloud deployment (optional)
- **AWS EC2**: Self-hosted deployment (optional)

---

## 🚢 Deployment

### Development
```bash
cd backend
python manage.py runserver
```

### Production (Heroku)
```bash
heroku create xstn-api
heroku config:set DEBUG=False
git push heroku main
heroku run python manage.py migrate
```

See [Deployment Guide](./backend/BACKEND_SETUP.md#deployment-guide) for AWS EC2, Docker, and other options.

---

## 📊 Database Schema

### User Model
- Extended Django User with email verification
- Password reset tokens
- Failed login tracking and account locking
- Last login metadata

### Form Models (8 Total)
1. **ContactForm**: name, email, phone, subject, message
2. **InquiryForm**: name, email, company, project_type, budget_range, timeline, message
3. **InternshipApplication**: full_name, email, phone, university, skills, experience, portfolio_url, resume_url
4. **DeveloperApplication**: full_name, email, phone, role_interested, experience_level, skills, portfolio_url, github_url, message
5. **JoinApplication**: full_name, email, role_interested, why_join
6. **ConsultationRequest**: full_name, email, phone, consultation_type, preferred_date, requirement
7. **NewsletterSubscription**: email, is_active
8. **Testimonial**: name, company, email, rating, message, is_approved

---

## 🔐 Security Features

- **CORS Configuration**: Restricted to allowed domains
- **Password Hashing**: Using Django's default password hasher
- **JWT Authentication**: Secure token-based auth
- **Email Verification**: Two-factor email confirmation
- **Account Locking**: After 5 failed login attempts
- **HTTPS Ready**: Production configuration included
- **SQL Injection Protection**: Django ORM prevents attacks
- **CSRF Protection**: Enabled by default

---

## 🤝 API Client Usage

### Installation
The `api-client.js` file is already in the frontend folder and ready to use.

### Import Functions
```javascript
import {
    submitContactForm,
    submitInquiryForm,
    submitInternshipApplication,
    submitDeveloperApplication,
    submitJoinApplication,
    submitConsultationRequest,
    subscribeNewsletter,
    submitTestimonial,
    validateContactForm,
    showSuccessMessage,
    showErrorMessage
} from './api-client.js';
```

### Example Usage
```javascript
const result = await submitContactForm({
    name: 'John Doe',
    email: 'john@example.com',
    phone: '+1234567890',
    subject: 'Inquiry',
    message: 'Hello, I have a question.'
});

if (result.success) {
    showSuccessMessage('Form submitted successfully!');
} else {
    showErrorMessage(result.error);
}
```

---

## 📈 Project Statistics

- **Frontend Files**: 10 HTML pages + 7 JS/CSS files
- **Backend Files**: 50+ Python files
- **Database Models**: 9 total (1 User + 8 Form models)
- **API Endpoints**: 8+ endpoints with full CRUD
- **Serializers**: 8 serializers for form data
- **Test Cases**: 64+ comprehensive tests
- **Documentation**: 5+ markdown guides

---

## 🎓 Learning Resources

### Django & DRF
- [Django Official Docs](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Django Best Practices](https://docs.djangoproject.com/en/stable/topics/db/models/best-practices/)

### Frontend
- [MDN Web Docs](https://developer.mozilla.org/)
- [JavaScript Modules](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules)
- [Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)

---

## 🐛 Troubleshooting

### Frontend Issues
- **CORS Error**: Update `CORS_ALLOWED_ORIGINS` in backend settings
- **404 API Errors**: Ensure backend is running on correct port
- **Form Not Submitting**: Check browser console for validation errors

### Backend Issues
- **Migration Errors**: Run `python manage.py migrate --noinput`
- **Email Not Sending**: Verify Gmail app password
- **Database Locked**: Delete `db.sqlite3` and run migrations again

See full troubleshooting in:
- [Backend Setup Guide](./backend/BACKEND_SETUP.md#troubleshooting)
- [API Integration Guide](./frontend/API_INTEGRATION.md#troubleshooting)

---

## 📞 Support

### Documentation
- Read the detailed guides in each folder
- Check API documentation for endpoint details
- Review test files for usage examples

### Common Commands

```bash
# Backend
cd backend
python manage.py runserver              # Start development server
python manage.py test                   # Run all tests
python manage.py makemigrations         # Create migrations
python manage.py migrate                # Apply migrations
python manage.py createsuperuser        # Create admin user
python manage.py shell                  # Django shell

# Frontend
# Just open HTML files in browser
# No build process needed
```

---

## 📝 Version History

### v1.0 - Current Release
- ✅ Frontend: 10 pages + 8 forms + modern auth
- ✅ Backend: 9 models + 8 serializers + full API
- ✅ Tests: 64+ test cases
- ✅ Documentation: Complete setup & deployment guides
- ✅ API Client: Ready-to-use JavaScript library
- ✅ Integration: Full frontend-backend integration

---

## 📄 License

This project is part of XSTN (Student Tech Network). All rights reserved.

---

## 🎉 Ready to Go!

Your XSTN project is now fully configured with:
- ✅ Complete backend API with 8 form endpoints
- ✅ Full frontend with modern authentication
- ✅ Comprehensive API documentation
- ✅ Ready-to-use JavaScript API client
- ✅ 64+ test cases
- ✅ Deployment guides

**Next Steps**:
1. [Start the backend](./backend/BACKEND_SETUP.md)
2. [Open the frontend](./frontend/README.md)
3. [Review API Documentation](./backend/API_DOCUMENTATION.md)
4. [Integrate forms with API](./frontend/API_INTEGRATION.md)
5. [Deploy to production](./backend/BACKEND_SETUP.md#deployment-guide)

---

**Last Updated**: January 2024
**Status**: Production Ready ✅
