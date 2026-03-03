# XSTN Backend API

Professional FastAPI backend with PostgreSQL, JWT authentication, and form handling for XSTN.

## Features

- **FastAPI** - High-performance async web framework
- **PostgreSQL** - Secure relational database
- **JWT Authentication** - Secure token-based authentication
- **CORS Protection** - Cross-origin security
- **Email Service** - Contact form notifications and confirmations
- **Admin Dashboard Support** - Ready for admin panel integration
- **Rate Limiting** - Protection against abuse
- **Security Best Practices** - Password hashing, HTTPS support, etc.

## Project Structure

```
backend/
├── app/
│   ├── core/
│   │   ├── config.py          # Configuration management
│   │   ├── database.py        # Database connection
│   │   └── security.py        # JWT and encryption utilities
│   ├── models/
│   │   ├── user.py            # User model
│   │   ├── contact.py         # Contact & Inquiry forms
│   │   └── internship.py       # Internship applications
│   ├── schemas/               # Pydantic request/response schemas
│   ├── routes/
│   │   ├── auth.py            # Authentication endpoints
│   │   └── forms.py           # Form submission endpoints
│   └── services/
│       ├── user_service.py    # User business logic
│       ├── form_service.py    # Form handling logic
│       └── email_service.py   # Email notifications
├── main.py                    # FastAPI application entry point
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
└── README.md                 # This file
```

## Installation

### 1. Setup Virtual Environment

```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` with your configuration:
```
DATABASE_URL=postgresql://user:password@localhost:5432/xstn_db
SECRET_KEY=your-super-secret-key
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FRONTEND_URL=http://localhost:3000
```

### 4. Setup PostgreSQL Database

```bash
# Install PostgreSQL (if not already installed)
# macOS: brew install postgresql
# Windows: Download from https://www.postgresql.org/download/windows/
# Linux: sudo apt-get install postgresql

# Create database
createdb xstn_db

# Or using psql
psql
CREATE DATABASE xstn_db;
```

### 5. Run the Application

```bash
uvicorn main:app --reload
```

The API will be available at: `http://localhost:8000`

API Documentation (Swagger UI): `http://localhost:8000/docs`

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get tokens
- `POST /api/auth/refresh` - Refresh access token

### Forms
- `POST /api/forms/contact` - Submit contact form
- `POST /api/forms/inquiry` - Submit inquiry/proposal request
- `POST /api/forms/internship` - Submit internship application
- `GET /api/forms/contact` - Get all contact forms (admin)
- `GET /api/forms/inquiry` - Get all inquiry forms (admin)
- `GET /api/forms/internship` - Get all internship applications (admin)

### Health
- `GET /` - Root health check
- `GET /health` - Health status

## Email Configuration

### Gmail Setup (Recommended for development)

1. Enable 2-factor authentication on Gmail
2. Generate an App Password: https://myaccount.google.com/apppasswords
3. Use App Password in `.env` as SMTP_PASSWORD

```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-16-character-app-password
```

## Database Migrations (Future)

To add Alembic migrations (optional):

```bash
pip install alembic
alembic init migrations
```

## Deployment

### Production Checklist

- [ ] Update `SECRET_KEY` to a strong random value
- [ ] Set `DEBUG=False` and `ENVIRONMENT=production`
- [ ] Use environment-specific database credentials
- [ ] Configure proper SMTP/email service
- [ ] Set up SSL/HTTPS certificates
- [ ] Configure allowed hosts in CORS
- [ ] Use a production ASGI server (Gunicorn + Uvicorn)

### Using Gunicorn

```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000
```

## Security Features

✅ Password hashing with bcrypt
✅ JWT token authentication
✅ CORS middleware
✅ Trusted host middleware
✅ SQL injection prevention (SQLAlchemy ORM)
✅ Email validation
✅ HTTPS-ready
✅ SQL connection pooling
✅ Async operations for better performance

## Testing

To test endpoints, use the interactive Swagger UI at `/docs` or create a test file:

```python
import httpx

async def test_contact_form():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/forms/contact",
            json={
                "name": "John Doe",
                "email": "john@example.com",
                "subject": "Test",
                "message": "Test message"
            }
        )
        print(response.json())
```

## Troubleshooting

**Database Connection Error**
- Check PostgreSQL is running: `psql --version`
- Verify DATABASE_URL in `.env`
- Check database exists: `psql -l`

**Email Not Sending**
- Verify SMTP credentials in `.env`
- Check Gmail App Passwords are configured correctly
- Allow "less secure apps" if not using App Password

**Port Already in Use**
```bash
# Change port
uvicorn main:app --port 8001
```

## Support

For issues or questions, contact: contact@xstn.tech

---

Built with ❤️ by XSTN - Xplorevo Student Tech Network
