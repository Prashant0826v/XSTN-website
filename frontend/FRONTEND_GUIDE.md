# XSTN Frontend JavaScript Guide

## Overview

The XSTN frontend is a static website with integrated JavaScript for form handling, API communication, and user interactions. All forms are connected to the FastAPI backend for data collection and email notifications.

## File Structure

```
frontend/
├── config.js          - API endpoints and configuration
├── form.js            - Contact, proposal, consultation form handlers
├── join.js            - Internship join form handler
├── utils.js           - Utility functions for form handling
├── runtime-config.js  - Runtime environment configuration
├── style.css          - Main stylesheet
├── index.html         - Home page
├── contact.html       - Contact form page
├── proposal.html      - Proposal request form
├── consultation.html  - Consultation request form
├── internship.html    - Internship application form
├── join.html          - Join developer form (internship)
└── join-developer.html - Join as developer form
```

## JavaScript Files Description

### config.js
- **Purpose**: Centralizes API endpoint configuration
- **Features**:
  - Detects environment (localhost vs production)
  - Supports runtime API URL override via `window.API_BASE_URL`
  - Configures CORS headers and request options
  - Exports `API_ENDPOINTS` and `REQUEST_OPTIONS`

**Key Variables**:
```javascript
API_BASE_URL              // Base URL for backend API
API_ENDPOINTS.CONTACT     // POST /api/forms/contact
API_ENDPOINTS.INQUIRY     // POST /api/forms/inquiry
API_ENDPOINTS.INTERNSHIP  // POST /api/forms/internship
REQUEST_OPTIONS           // Default headers and CORS settings
```

### form.js
- **Purpose**: Handles all form submissions (contact, proposal, consultation, internship)
- **Features**:
  - Input validation and trimming
  - Error handling with user feedback
  - Loading states on submit buttons
  - Shows/hides success messages
  - Smooth scrolling to feedback

**Handled Forms**:
- Contact form (#contactForm) → POST /api/forms/contact
- Proposal form (.proposal-form) → POST /api/forms/inquiry
- Consultation form (.consult-form) → POST /api/forms/inquiry
- Internship form (#internshipForm) → POST /api/forms/internship

### join.js
- **Purpose**: Handles join/internship program form submissions
- **Features**:
  - Maps form data to internship application schema
  - Shows success modal on completion
  - Validates required fields

**Handles**: #joinForm → POST /api/forms/internship

### utils.js
- **Purpose**: Shared utility functions for form handling
- **Exports**:
  - `isValidEmail()` - Email validation
  - `isValidPhone()` - Phone validation
  - `trimFormValues()` - Trim all form inputs
  - `setButtonLoading()` - Show loading state
  - `showNotification()` - Toast notifications
  - `handleApiError()` - API error handling
  - `disableForm()` - Disable form during submission
  - `getFormData()` - Extract form data as object

### runtime-config.js
- **Purpose**: Optional runtime configuration override
- **Usage**: Set `window.API_BASE_URL` for production backend URL

## Form Integration

### Connecting a Form to the Backend

All forms must include these three scripts before closing `</body>`:

```html
<script src="runtime-config.js"></script>
<script src="config.js"></script>
<script src="form.js"></script>  <!-- or join.js -->
```

### Required Form Structure

Each form must have:
1. Unique `id` or `class` identifier
2. Named input fields matching the backend schema
3. Submit button (type="submit")
4. Success message element (optional but recommended)

**Example**:
```html
<form id="contactForm">
  <div class="form-group">
    <label>Name</label>
    <input type="text" name="full_name" required>
  </div>
  
  <div class="form-group">
    <label>Email</label>
    <input type="email" name="email" required>
  </div>
  
  <button type="submit" class="submit-btn">Submit</button>
</form>

<div class="success-message" id="contactSuccess" style="display: none;">
  <p>✅ Message sent successfully!</p>
</div>
```

## API Endpoints

All endpoints are prefixed with the backend base URL (default: `http://127.0.0.1:8000`).

### POST /api/forms/contact
**Purpose**: Submit contact form messages

**Request Body**:
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "subject": "Inquiry",
  "message": "I need help with..."
}
```

**Response**:
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "is_read": false,
  "created_at": "2024-02-27T10:30:00"
}
```

### POST /api/forms/inquiry
**Purpose**: Submit proposal/inquiry requests

**Request Body**:
```json
{
  "name": "Jane Doe",
  "email": "jane@example.com",
  "company": "Tech Startup",
  "project_type": "website",
  "budget_range": "10k_30k",
  "timeline": "2 months",
  "message": "We need a custom website..."
}
```

**Response**: Same structure as contact form

### POST /api/forms/internship
**Purpose**: Submit internship applications

**Request Body**:
```json
{
  "full_name": "John Student",
  "email": "student@university.edu",
  "phone": "+1234567890",
  "university": "XYZ University",
  "skills": "HTML, CSS, JavaScript, React",
  "experience": "I have 2 years of web development experience...",
  "portfolio_url": "https://github.com/username",
  "resume_url": null
}
```

**Response**:
```json
{
  "id": 1,
  "full_name": "John Student",
  "email": "student@university.edu",
  "status": "pending",
  "is_read": false,
  "created_at": "2024-02-27T10:30:00"
}
```

## Environment Configuration

### Development (Local)
```javascript
// Automatic detection when running on localhost
API_BASE_URL = "http://127.0.0.1:8000"
```

### Production (Live Server)
Add to `runtime-config.js` before other scripts load:
```javascript
window.API_BASE_URL = "https://your-backend-domain.com";
```

Or add meta tag to HTML head:
```html
<meta name="api-base-url" content="https://your-backend-domain.com">
```

## Error Handling

All forms include comprehensive error handling:

1. **Network Errors**: Display user-friendly message
2. **Validation Errors**: Show inline field errors
3. **Server Errors**: Display error response message

**Examples**:
```javascript
// Bad Request (validation error)
{
  "detail": "Invalid email format"
}

// Internal Server Error
{
  "detail": "Database connection failed"
}
```

## Testing Forms Locally

### 1. Start Backend
```bash
cd backend
uvicorn main:app --reload
```

### 2. Open Frontend in Browser
```
http://localhost:5500/ (Live Server)
or
file:///path/to/frontend/index.html
```

### 3. Submit Test Form
- Navigate to any form page
- Fill in required fields
- Click submit
- Check console (F12) for API response
- Backend logs should show the submission

### 4. Verify Emails Sent
- Check inbox for confirmation emails
- Check spam folder if needed

## Form States

### Idle State
- Form inputs enabled
- Submit button text: "Submit" / "Apply Now" / etc.

### Loading State
- Form inputs disabled
- Submit button text: "Sending..." / "Submitting..." / "Applying..."
- Button disabled and shows loading indicator

### Success State
- Form hidden
- Success message displayed
- Smooth scroll to success message
- Optional: Clear form data

### Error State
- Form remains visible
- Error message displayed in alert
- Button re-enabled for retry

## Customization

### Changing API Endpoints
Edit `config.js`:
```javascript
const API_ENDPOINTS = {
  CONTACT: `${API_BASE_URL}/api/forms/contact`,
  INQUIRY: `${API_BASE_URL}/api/forms/inquiry`,
  // Add more endpoints as needed
};
```

### Modifying Validation
Edit form handlers in `form.js`:
```javascript
// Add custom validation before fetch
if(!customValidation(formData)) {
  alert("Custom error message");
  return;
}
```

### Custom Success Messages
Edit form element structure:
```html
<div class="success-message" id="customSuccess" style="display: none;">
  <h3>✅ Success!</h3>
  <p>Custom message here...</p>
</div>
```

## Troubleshooting

### Forms Not Submitting
1. Check browser console (F12) for errors
2. Verify backend is running: `http://localhost:8000/health`
3. Check CORS settings in backend
4. Verify form `id` or `class` matches JavaScript handler

### API Errors
1. Check `API_BASE_URL` in config
2. Verify backend endpoint exists
3. Check request body matches schema
4. Look at backend logs for details

### Emails Not Sending
1. Check SMTP configuration in backend `.env`
2. Verify email credentials
3. Check spam folder
4. Check backend logs for email errors

### CORS Errors
1. Verify `FRONTEND_URL` in backend `.env`
2. Check CORS middleware in `main.py`
3. Ensure request headers match backend settings

## Performance Tips

1. **Minify JavaScript**: Use terser or webpack
2. **Load scripts async**: Add `async` attribute if needed
3. **Cache API responses**: Implement caching for repeated requests
4. **Debounce form submissions**: Prevent double submissions
5. **Optimize images**: Use modern formats (WebP, AVIF)

## Security Considerations

✅ **Already Implemented**:
- CORS validation on backend
- Input sanitization at backend
- Rate limiting ready in FastAPI
- Secure headers in response
- Email validation

✅ **Best Practices**:
- Never store sensitive data in localStorage
- Always validate on backend
- Use HTTPS in production
- Implement rate limiting
- Monitor form submissions

## Future Enhancements

- [ ] Add real-time form validation
- [ ] Implement file upload for resume
- [ ] Add form progress indicators
- [ ] Create admin dashboard for submissions
- [ ] Add analytics tracking
- [ ] Implement form pre-filling
- [ ] Add captcha for spam prevention
- [ ] Support multiple languages

## Support

For issues or questions:
- Check browser console for errors
- Review backend logs
- Contact: contact@xstn.tech

---

Last Updated: February 2026
Built with ❤️ by XSTN
