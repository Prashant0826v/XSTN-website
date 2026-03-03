# XSTN Django Backend

**Status**: ✅ Converted from FastAPI to Django  
**Framework**: Django 4.2 + Django REST Framework  
**Database**: PostgreSQL  

---

## 🚀 Quick Start (5 minutes)

### 1. Setup Environment
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 2. Configure Database
```bash
# Create PostgreSQL database
createdb xstn_db

# Or using psql:
psql -U postgres
CREATE DATABASE xstn_db;
```

### 3. Configure .env
```bash
cp .env.example .env
# Edit .env with your database and email credentials
```

### 4. Run Migrations
```bash
python manage.py migrate
```

### 5. Create Admin User
```bash
python manage.py createsuperuser
# Follow prompts to create admin account
```

### 6. Start Server
```bash
python manage.py runserver
```

**Access**:
- API: http://localhost:8000
- Admin: http://localhost:8000/admin
- Health: http://localhost:8000/health

---

## 📁 Project Structure

```
backend/
├── manage.py                  - Django CLI
├── config/                    - Project settings
│   ├── settings.py           - Django configuration
│   ├── urls.py               - URL routing
│   ├── wsgi.py               - WSGI application
│   └── asgi.py               - ASGI application
├── apps/
│   ├── users/                - User management app
│   │   ├── models.py         - Extended User model
│   │   ├── views.py          - User viewsets
│   │   ├── serializers.py    - DRF serializers
│   │   └── admin.py          - Django admin config
│   └── forms/                - Form submissions app
│       ├── models.py         - ContactForm, InquiryForm, InternshipApplication
│       ├── views.py          - Form viewsets & email logic
│       ├── serializers.py    - DRF serializers
│       └── admin.py          - Django admin config
├── requirements.txt          - Python dependencies
└── .env.example             - Environment template
```

---

## 🔗 API Endpoints

### Authentication
```
POST   /api/token/                  - Get access token (JWT login)
POST   /api/token/refresh/          - Refresh access token
POST   /api/users/register/         - Register new user
GET    /api/users/me/               - Get current user
```

### Contact Forms
```
POST   /api/forms/contact/          - Submit contact form
GET    /api/forms/contact/          - List all (admin only)
GET    /api/forms/contact/{id}/     - Get detail
```

### Inquiry Forms
```
POST   /api/forms/inquiry/          - Submit inquiry/proposal
GET    /api/forms/inquiry/          - List all (admin only)
GET    /api/forms/inquiry/{id}/     - Get detail
```

### Internship Applications
```
POST   /api/forms/internship/       - Submit application
GET    /api/forms/internship/       - List all (admin only)
PATCH  /api/forms/internship/{id}/  - Update status
```

### Health
```
GET    /                            - Root check
GET    /health/                     - Health status
```

---

## 📊 Database Models

### User (Extended Django User)
- `username` - Unique username
- `email` - Unique email
- `first_name`, `last_name`
- `phone`, `company`, `bio`
- `is_verified` - Email verification status
- `created_at`, `updated_at`

### ContactForm
- `name`, `email`, `phone`
- `subject`, `message`
- `is_read` - Admin marker
- `created_at`

### InquiryForm
- `name`, `email`, `company`
- `project_type`, `budget_range`, `timeline`
- `message`, `is_read`, `created_at`

### InternshipApplication
- `full_name`, `email`, `phone`
- `university`, `skills`, `experience`
- `portfolio_url`, `resume_url`
- `status` - pending/reviewed/selected/rejected
- `notes`, `is_read`, `created_at`

---

## 🔐 Authentication (JWT)

### Get Token (Login)
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"user","password":"password"}'
```

Response:
```json
{
  "access": "eyJ0...",
  "refresh": "eyJ0..."
}
```

### Use Token in Requests
```bash
curl http://localhost:8000/api/users/me/ \
  -H "Authorization: Bearer eyJ0..."
```

### Refresh Token
```bash
curl -X POST http://localhost:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh":"eyJ0..."}'
```

---

## 📧 Email Configuration

### Gmail (Recommended)
1. Enable 2-Factor Authentication
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Update `.env`:
```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=<16-char-app-password>
FROM_EMAIL=noreply@xstn.tech
```

### Other Providers
Use SendGrid, AWS SES, Mailgun, or any SMTP provider.

---

## 🎯 Admin Dashboard

Access at: http://localhost:8000/admin

**Login with**:
- Username: (created with `createsuperuser`)
- Password: (created with `createsuperuser`)

**Features**:
- ✅ View all form submissions
- ✅ Mark submissions as read
- ✅ Update internship application status
- ✅ Manage users
- ✅ Bulk actions

---

## 🧪 Testing Forms

### Test Contact Form
```bash
curl -X POST http://localhost:8000/api/forms/contact/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "subject": "Website Inquiry",
    "message": "I need a new website"
  }'
```

### Test Internship Application
```bash
curl -X POST http://localhost:8000/api/forms/internship/ \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Jane Student",
    "email": "jane@university.edu",
    "phone": "+1234567890",
    "university": "Digital University",
    "skills": "Python, Django, React, PostgreSQL",
    "experience": "1 year freelance web development",
    "portfolio_url": "https://github.com/janestudent"
  }'
```

---

## 🚀 Deployment

### Pre-Deployment
```bash
# Create strong SECRET_KEY
python manage.py shell
>>> from django.core.management.utils import get_random_secret_key
>>> get_random_secret_key()
# Copy output to .env
```

### Using Gunicorn
```bash
pip install gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

### Production Settings
```python
# config/settings.py
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'api.yourdomain.com']
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### Heroku Deployment
```bash
heroku create xstn-api
heroku addons:create heroku-postgresql:hobby-dev
heroku config:set SECRET_KEY="your-key"
heroku config:set DEBUG=False
git push heroku main
heroku run python manage.py migrate
```

---

## 🛠️ Useful Commands

```bash
# Migrations
python manage.py makemigrations
python manage.py migrate
python manage.py migrate apps forms zero  # Reset migrations

# Admin
python manage.py createsuperuser
python manage.py changepassword username

# Database
python manage.py dbshell               # PostgreSQL CLI
python manage.py dumpdata > backup.json
python manage.py loaddata backup.json

# Development
python manage.py runserver 0.0.0.0:8000
python manage.py shell                # Python REPL with Django context
python manage.py test                 # Run tests

# Static files
python manage.py collectstatic
```

---

## 🔒 Security Features

✅ Django's built-in CSRF protection  
✅ XSS prevention  
✅ SQL injection prevention (ORM)  
✅ Password hashing with PBKDF2  
✅ JWT token authentication  
✅ CORS validation  
✅ Secure headers  
✅ Session security  

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :8000
kill -9 <PID>
```

### Database Connection Error
```bash
# Verify PostgreSQL running
# Windows: Services panel
# macOS: brew services list
# Linux: systemctl status postgresql

# Check .env credentials
# Test connection: psql -U postgres -d xstn_db
```

### Migration Issues
```bash
# Clear migrations (development only)
python manage.py migrate apps forms zero
python manage.py migrate
```

### Email Not Sending
- Verify SMTP credentials in `.env`
- Check Gmail App Password is correct
- Try: `python manage.py shell` then `from django.core.mail import send_mail`

---

## 📚 Frontend Integration

Update `frontend/config.js`:
```javascript
const API_BASE_URL = 'http://localhost:8000';
```

All forms will now POST to:
- `/api/forms/contact/`
- `/api/forms/inquiry/`
- `/api/forms/internship/`

---

## 📞 Support

- **Framework Docs**: https://docs.djangoproject.com
- **DRF Docs**: https://www.django-rest-framework.org
- **JWT Docs**: https://github.com/jpadilla/django-rest-framework-simplejwt

---

**Status**: ✅ Production Ready  
**Built**: February 2026  
**Team**: XSTN
