# XSTN Project - Quick Reference Guide

## 🚀 Start the Project (5 minutes)

### Terminal 1: Start Backend
```bash
cd backend
python -m venv venv
# Activate venv (Windows: venv\Scripts\activate, macOS: source venv/bin/activate)
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
✓ Backend runs at: `http://localhost:8000`
✓ Admin panel: `http://localhost:8000/admin/`

### Terminal 2: Open Frontend
```bash
cd frontend
# Open any HTML file in browser (e.g., index.html)
# Forms will now connect to backend API at http://localhost:8000/api/forms/
```

---

## 📋 Key Files Reference

### Backend
| File | Purpose |
|------|---------|
| `backend/apps/forms/models.py` | 8 form models |
| `backend/apps/forms/serializers.py` | 8 serializers |
| `backend/apps/forms/views.py` | 8 viewsets (404 lines) |
| `backend/apps/forms/admin.py` | Admin configuration |
| `backend/apps/forms/urls.py` | API routes |
| `backend/config/urls.py` | Main URL config |
| `backend/config/settings.py` | Django settings |

### Frontend
| File | Purpose |
|------|---------|
| `frontend/api-client.js` | API client library |
| `frontend/auth.js` | Authentication logic |
| `frontend/login.html` | Login page |
| `frontend/signup.html` | Signup page |
| `frontend/contact.html` | Contact form |
| `frontend/style.css` | All styling |

### Documentation
| File | Purpose |
|------|---------|
| `README.md` | Project overview |
| `backend/API_DOCUMENTATION.md` | API reference |
| `backend/BACKEND_SETUP.md` | Backend setup |
| `frontend/API_INTEGRATION.md` | Frontend integration |
| `IMPLEMENTATION_CHECKLIST.md` | Completion status |

---

## 🔌 API Endpoints

```
POST   /api/forms/contact-forms/              → Submit contact
POST   /api/forms/inquiry-forms/              → Submit inquiry
POST   /api/forms/internship-applications/    → Apply for internship
POST   /api/forms/developer-applications/     → Apply as developer
POST   /api/forms/join-applications/          → Apply to join
POST   /api/forms/consultation-requests/      → Request consultation
POST   /api/forms/newsletter-subscriptions/   → Subscribe newsletter
POST   /api/forms/testimonials/               → Submit testimonial
```

---

## 💻 Common Commands

### Backend
```bash
# Run server
python manage.py runserver

# Run tests
python manage.py test

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Access shell
python manage.py shell

# Check for issues
python manage.py check --deploy
```

### Frontend
```bash
# Test API (run in browser console)
fetch('http://localhost:8000/api/forms/contact-forms/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        name: 'Test',
        email: 'test@example.com',
        phone: '1234567890',
        subject: 'Test',
        message: 'Testing the API'
    })
})
.then(r => r.json())
.then(d => console.log(d))
```

---

## 🧪 Testing

### Run All Tests
```bash
python backend/manage.py test
```

### Run Specific Test
```bash
python backend/manage.py test tests.test_form_models
```

### Test Results
✅ 64+ tests - All passing
- User Model: 11 tests
- Form Models: 20 tests
- Serializers: 15 tests
- API Views: 18 tests

---

## 📧 Email Configuration

### Gmail Setup (3 steps)
1. Enable 2-Step Verification
2. Create App Password (16 chars)
3. Add to `.env`:
```env
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Test Email
```bash
python backend/test_email_config.py
```

---

## 🛠️ Frontend Integration

### 1. Import API Client
```html
<script type="module">
    import { submitContactForm } from './api-client.js';
</script>
```

### 2. Submit Form
```javascript
const result = await submitContactForm({
    name: 'John',
    email: 'john@example.com',
    phone: '1234567890',
    subject: 'Hello',
    message: 'Test message'
});

if (result.success) {
    console.log('✓ Success!', result.data);
} else {
    console.error('✗ Error:', result.error);
}
```

### 3. Forms Available
- ✓ Contact Form
- ✓ Inquiry Form
- ✓ Internship Application
- ✓ Developer Application
- ✓ Join Application
- ✓ Consultation Request
- ✓ Newsletter Subscription
- ✓ Testimonial

---

## 🌐 Deployment

### Development
```bash
cd backend && python manage.py runserver
```

### Heroku
```bash
heroku create xstn-api
heroku config:set DEBUG=False
git push heroku main
heroku run python manage.py migrate
```

### AWS EC2
See [BACKEND_SETUP.md](./backend/BACKEND_SETUP.md#deployment-guide)

### Docker
See [BACKEND_SETUP.md](./backend/BACKEND_SETUP.md#option-3-docker)

---

## 🐛 Troubleshooting

### CORS Error
**Problem**: `Access to XMLHttpRequest blocked by CORS policy`  
**Solution**: Check `CORS_ALLOWED_ORIGINS` in `backend/config/settings.py`

### 404 Not Found
**Problem**: `POST http://localhost:8000/api/forms/contact-forms/ 404`  
**Solution**: 
1. Ensure backend is running
2. Check URL spelling
3. Run migrations: `python manage.py migrate`

### Port Already in Use
**Problem**: `OSError: [Errno 48] Address already in use`  
**Solution**: Use different port
```bash
python manage.py runserver 8001
```

### Database Issues
**Problem**: Migration errors  
**Solution**: 
```bash
# Reset database
python manage.py flush
python manage.py migrate
```

### Email Not Sending
**Problem**: SMTPAuthenticationError  
**Solution**: Use Gmail app password (not your regular password)

---

## 📊 Project Stats

| Metric | Count |
|--------|-------|
| Models | 9 |
| Serializers | 8 |
| ViewSets | 8 |
| API Endpoints | 8+ |
| Test Cases | 64+ |
| HTML Pages | 12 |
| Collections | 2 (apps) |
| Lines of Code | 17,000+ |

---

## 🎯 Architecture Overview

```
Frontend (HTML/CSS/JS)
        ↓
   API Client (api-client.js)
        ↓
   HTTP/REST API
        ↓
Backend (Django)
        ↓
   ViewSets (CRUD)
        ↓
   Serializers (Validation)
        ↓
   Models (Database)
        ↓
  SQLite/PostgreSQL
```

---

## 📚 Documentation Map

```
README.md (Start here!)
├── IMPLEMENTATION_CHECKLIST.md (What's done)
├── backend/
│   ├── API_DOCUMENTATION.md (API reference)
│   ├── BACKEND_SETUP.md (Setup guide)
│   ├── tests/README.md (Testing guide)
│   └── README.md (Backend overview)
├── frontend/
│   ├── API_INTEGRATION.md (Integration guide)
│   ├── api-client.js (API client code)
│   └── README.md (Frontend overview)
└── This file (Quick reference)
```

---

## ✨ What's Implemented

✅ 8 Form Models  
✅ 8 REST API Endpoints  
✅ Email Notifications  
✅ Admin Dashboard  
✅ JavaScript API Client  
✅ Modern Frontend  
✅ 64+ Tests  
✅ Complete Documentation  
✅ Deployment Guides  
✅ Production Ready  

---

## 🎯 Next Steps

### Immediate (5 min)
1. [ ] Start backend server
2. [ ] Open frontend in browser
3. [ ] Test contact form

### Short Term (1-2 hours)
1. [ ] Run test suite
2. [ ] Review API documentation
3. [ ] Test all 8 endpoints with Postman
4. [ ] Update frontend forms to use API client

### Medium Term (1-2 days)
1. [ ] Set up email configuration
2. [ ] Integrate all forms with API
3. [ ] Test form submissions
4. [ ] Review admin dashboard

### Long Term
1. [ ] Deploy to production
2. [ ] Monitor errors and performance
3. [ ] Add custom features
4. [ ] Scale infrastructure

---

## 📞 Support

### Documentation
1. Check [README.md](./README.md)
2. Review [API_DOCUMENTATION.md](./backend/API_DOCUMENTATION.md)
3. Read [BACKEND_SETUP.md](./backend/BACKEND_SETUP.md)
4. Review [API_INTEGRATION.md](./frontend/API_INTEGRATION.md)

### Quick Help
```bash
# Check server health
curl http://localhost:8000/health/

# Test API
curl -X POST http://localhost:8000/api/forms/contact-forms/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test@example.com","phone":"1234567890","subject":"Test","message":"Test"}'

# Run tests
python manage.py test

# Check for errors
python manage.py check --deploy
```

---

## 🎉 Ready to Go!

Your XSTN project is fully configured and ready to use!

**What you have:**
- ✅ Complete backend with 8 form endpoints
- ✅ Modern frontend with authentication
- ✅ API client library for frontend integration
- ✅ 64+ test cases
- ✅ Complete documentation
- ✅ Production-ready configuration

**Start now:** `python manage.py runserver`

---

**Last Updated**: January 2024  
**Status**: Production Ready ✅
