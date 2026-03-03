# XSTN Backend - Setup & Deployment Guide

## Table of Contents
1. [Environment Setup](#environment-setup)
2. [Installation & Configuration](#installation--configuration)
3. [Database Migration](#database-migration)
4. [Running the Development Server](#running-the-development-server)
5. [Email Configuration](#email-configuration)
6. [Deployment Guide](#deployment-guide)
7. [Troubleshooting](#troubleshooting)

---

## Environment Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- PostgreSQL 12+ (optional, SQLite used in development)
- Git
- Virtual Environment (recommended)

### Step 1: Clone Repository
```bash
cd ~/Desktop
git clone <repository-url>
cd XSTN\ Project/backend
```

### Step 2: Create Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Upgrade pip
```bash
python -m pip install --upgrade pip
```

---

## Installation & Configuration

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Create Environment Variables
Create a `.env` file in the backend root directory:

```env
# Django Settings
DEBUG=True
SECRET_KEY=your-super-secret-key-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
# For SQLite (default):
DATABASE_ENGINE=django.db.backends.sqlite3
DATABASE_NAME=db.sqlite3

# For PostgreSQL (optional):
# DATABASE_ENGINE=django.db.backends.postgresql
# DATABASE_NAME=xstn_db
# DATABASE_USER=postgres
# DATABASE_PASSWORD=your_password
# DATABASE_HOST=localhost
# DATABASE_PORT=5432

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@xstn.com

# CORS Configuration
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# AWS Configuration (optional, for file uploads)
# AWS_ACCESS_KEY_ID=your-key
# AWS_SECRET_ACCESS_KEY=your-secret
# AWS_STORAGE_BUCKET_NAME=your-bucket

# JWT Configuration
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
```

### Step 3: Update settings.py
The `config/settings.py` should already have most configurations. Verify:

```python
# In settings.py
import os
from dotenv import load_dotenv

load_dotenv()

DEBUG = os.getenv('DEBUG', True)
SECRET_KEY = os.getenv('SECRET_KEY', 'your-default-secret-key')
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Database
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DATABASE_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.getenv('DATABASE_NAME', 'db.sqlite3'),
        'USER': os.getenv('DATABASE_USER', ''),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', ''),
        'HOST': os.getenv('DATABASE_HOST', ''),
        'PORT': os.getenv('DATABASE_PORT', ''),
    }
}

# Email Configuration
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', True)
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@xstn.com')

# CORS Configuration
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', 'http://localhost:3000').split(',')
```

---

## Database Migration

### Step 1: Create Migrations
```bash
python manage.py makemigrations
python manage.py makemigrations users
python manage.py makemigrations forms
```

### Step 2: Run Migrations
```bash
python manage.py migrate
```

### Step 3: Create Superuser
```bash
python manage.py createsuperuser
```

Or use the provided script:
```bash
python create_superuser.py
```

### Step 4: Verify Migrations
```bash
python manage.py showmigrations
```

---

## Running the Development Server

### Start the Server
```bash
python manage.py runserver
```

Server will be available at: `http://localhost:8000`

### Verify Server is Running
```bash
curl http://localhost:8000/
# Expected response: {"status": "healthy", "message": "XSTN Django API is running"}
```

### Access Admin Panel
- URL: `http://localhost:8000/admin/`
- Username: (your superuser username)
- Password: (your superuser password)

---

## Email Configuration

### Gmail Setup

#### Enable App Password
1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable 2-Step Verification
3. Create App Password
4. Copy the generated 16-character password

#### Update .env
```env
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-16-char-app-password
```

### Test Email Configuration
```bash
python manage.py shell

# In the Django shell:
from django.core.mail import send_mail
from django.conf import settings

send_mail(
    subject='XSTN Test Email',
    message='This is a test email from XSTN',
    from_email=settings.DEFAULT_FROM_EMAIL,
    recipient_list=['your-test-email@gmail.com'],
    fail_silently=False,
)
print("✓ Email sent successfully!")
```

Or run the test script:
```bash
python test_email_config.py
```

---

## Deployment Guide

### Deployment Platforms

#### Option 1: Heroku

##### Step 1: Install Heroku CLI
```bash
# macOS
brew tap heroku/brew && brew install heroku

# Windows
choco install heroku-cli
```

##### Step 2: Login to Heroku
```bash
heroku login
```

##### Step 3: Create Heroku App
```bash
heroku create xstn-api
```

##### Step 4: Set Environment Variables
```bash
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-production-secret-key
heroku config:set ALLOWED_HOSTS=xstn-api.herokuapp.com
heroku config:set EMAIL_HOST_USER=your-email@gmail.com
heroku config:set EMAIL_HOST_PASSWORD=your-app-password
```

##### Step 5: Deploy
```bash
git push heroku main
```

##### Step 6: Run Migrations
```bash
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

#### Option 2: AWS EC2

##### Step 1: Create EC2 Instance
- Use Ubuntu 20.04 LTS
- Allow ports 22 (SSH), 80 (HTTP), 443 (HTTPS)

##### Step 2: Connect and Setup
```bash
# SSH into instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3-pip python3-venv postgresql postgresql-contrib nginx -y
```

##### Step 3: Clone Repository
```bash
git clone <repository-url>
cd XSTN\ Project/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

##### Step 4: Configure Environment
```bash
nano .env
# Add production settings
```

##### Step 5: Database Setup
```bash
sudo -u postgres createdb xstn_db
python manage.py migrate
python manage.py createsuperuser
```

##### Step 6: Collect Static Files
```bash
python manage.py collectstatic --noinput
```

##### Step 7: Configure Nginx
```bash
sudo nano /etc/nginx/sites-available/default
```

Add configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location /static/ {
        alias /home/ubuntu/XSTN\ Project/backend/staticfiles/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

##### Step 8: Start Gunicorn
```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

#### Option 3: Docker

##### Step 1: Create Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```

##### Step 2: Create Docker Compose
```yaml
version: '3.8'

services:
  db:
    image: postgres:13
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: xstn_db
      POSTGRES_PASSWORD: postgres

  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      DATABASE_ENGINE: django.db.backends.postgresql
      DATABASE_NAME: xstn_db
      DATABASE_USER: postgres
      DATABASE_PASSWORD: postgres
      DATABASE_HOST: db

volumes:
  postgres_data:
```

##### Step 3: Build and Run
```bash
docker-compose build
docker-compose up
```

---

## Production Checklist

### Security
- [ ] Set `DEBUG = False`
- [ ] Use strong `SECRET_KEY`
- [ ] Add domain to `ALLOWED_HOSTS`
- [ ] Configure HTTPS/SSL
- [ ] Enable CORS only for allowed domains
- [ ] Set secure headers (HSTS, CSP, etc.)
- [ ] Use environment variables for secrets
- [ ] Regular security updates

### Performance
- [ ] Enable database query optimization
- [ ] Set up caching (Redis)
- [ ] Use CDN for static files
- [ ] Enable gzip compression
- [ ] Optimize database indexes
- [ ] Set up monitoring and logging

### Backup & Recovery
- [ ] Regular database backups
- [ ] Document backup/restore procedures
- [ ] Test recovery procedures
- [ ] Monitor disk space
- [ ] Set up automated backups

### Monitoring
- [ ] Error tracking (Sentry)
- [ ] Performance monitoring (New Relic)
- [ ] Uptime monitoring
- [ ] Log aggregation (ELK Stack)
- [ ] Alert system setup

---

## Troubleshooting

### Issue: ModuleNotFoundError
```
ModuleNotFoundError: No module named 'django'
```

**Solution**: Activate virtual environment
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Issue: Database Migration Error
```
django.db.utils.OperationalError: cannot open shared object file
```

**Solution**: Run migrations
```bash
python manage.py migrate
```

### Issue: Static Files Not Found
```
404 Not Found: /static/...
```

**Solution**: Collect static files
```bash
python manage.py collectstatic --noinput
```

### Issue: Email Not Sending
```
SMTPAuthenticationError: Application-specific password required
```

**Solution**: 
1. Use Gmail app password (not regular password)
2. Enable 2-Step Verification
3. Verify email configuration in `.env`

### Issue: Port Already in Use
```
OSError: [Errno 48] Address already in use
```

**Solution**: Use different port
```bash
python manage.py runserver 8001
```

Or kill existing process:
```bash
# macOS/Linux
lsof -ti:8000 | xargs kill -9

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Issue: CORS Error
```
Access to XMLHttpRequest blocked by CORS policy
```

**Solution**: Update `CORS_ALLOWED_ORIGINS`
```python
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'https://yourdomain.com'
]
```

### Issue: Import Error in Models
```
ImportError: cannot import make_password
```

**Solution**: Ensure proper imports
```python
from django.contrib.auth.hashers import make_password
```

---

## Useful Commands

```bash
# Run tests
python manage.py test

# Create superuser
python manage.py createsuperuser

# Reset database
python manage.py flush

# Generate API documentation
python manage.py generate_schema > api-schema.json

# Check for security issues
python manage.py check --deploy

# View all URLs
python manage.py show_urls

# Shell access
python manage.py shell

# Database backup (PostgreSQL)
pg_dump -U postgres xstn_db > backup.sql

# Database restore (PostgreSQL)
psql -U postgres xstn_db < backup.sql
```

---

## Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [Heroku Django Documentation](https://devcenter.heroku.com/articles/django-app-configuration)
- [AWS EC2 Best Practices](https://docs.aws.amazon.com/ec2/index.html)

---

## Support & Documentation

For issues or questions:
1. Check the [API Documentation](./API_DOCUMENTATION.md)
2. Review the [Testing Guide](./tests/README.md)
3. Check Django logs: `python manage.py runserver --verbosity=3`
4. Review database migrations: `python manage.py showmigrations`

---

**Last Updated**: 2024
**Version**: 1.0
