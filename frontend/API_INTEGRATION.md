# XSTN Frontend-Backend Integration Guide

## Overview
This guide explains how to connect your frontend forms to the XSTN Django backend API endpoints.

---

## API Base URL
```javascript
const API_BASE_URL = 'http://localhost:8000/api/forms';
```

---

## Form Submission Utility Function

Create a new file: `frontend/api-client.js`

```javascript
/**
 * XSTN API Client for form submissions
 */

const API_BASE_URL = 'http://localhost:8000/api/forms';

/**
 * Generic function to submit form data to API
 * @param {string} endpoint - API endpoint (e.g., 'contact-forms')
 * @param {object} data - Form data to submit
 * @returns {Promise} Response from server
 */
async function submitForm(endpoint, data) {
    try {
        const response = await fetch(`${API_BASE_URL}/${endpoint}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Form submission failed');
        }

        const result = await response.json();
        return {
            success: true,
            data: result
        };
    } catch (error) {
        console.error('API Error:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

/**
 * Submit contact form
 */
async function submitContactForm(formData) {
    return submitForm('contact-forms', {
        name: formData.name,
        email: formData.email,
        phone: formData.phone,
        subject: formData.subject,
        message: formData.message
    });
}

/**
 * Submit inquiry form
 */
async function submitInquiryForm(formData) {
    return submitForm('inquiry-forms', {
        name: formData.name,
        email: formData.email,
        company: formData.company,
        project_type: formData.projectType,
        budget_range: formData.budgetRange,
        timeline: formData.timeline,
        message: formData.message
    });
}

/**
 * Submit internship application
 */
async function submitInternshipApplication(formData) {
    return submitForm('internship-applications', {
        full_name: formData.fullName,
        email: formData.email,
        phone: formData.phone,
        university: formData.university,
        skills: formData.skills,
        experience: formData.experience,
        portfolio_url: formData.portfolioUrl,
        resume_url: formData.resumeUrl
    });
}

/**
 * Submit developer application
 */
async function submitDeveloperApplication(formData) {
    return submitForm('developer-applications', {
        full_name: formData.fullName,
        email: formData.email,
        phone: formData.phone,
        role_interested: formData.roleInterested,
        experience_level: formData.experienceLevel,
        skills: formData.skills,
        portfolio_url: formData.portfolioUrl,
        github_url: formData.githubUrl,
        message: formData.message
    });
}

/**
 * Submit join application
 */
async function submitJoinApplication(formData) {
    return submitForm('join-applications', {
        full_name: formData.fullName,
        email: formData.email,
        role_interested: formData.roleInterested,
        why_join: formData.whyJoin
    });
}

/**
 * Submit consultation request
 */
async function submitConsultationRequest(formData) {
    return submitForm('consultation-requests', {
        full_name: formData.fullName,
        email: formData.email,
        phone: formData.phone,
        consultation_type: formData.consultationType,
        preferred_date: formData.preferredDate,
        requirement: formData.requirement
    });
}

/**
 * Subscribe to newsletter
 */
async function subscribeNewsletter(email) {
    return submitForm('newsletter-subscriptions', {
        email: email
    });
}

/**
 * Submit testimonial
 */
async function submitTestimonial(formData) {
    return submitForm('testimonials', {
        name: formData.name,
        company: formData.company,
        email: formData.email,
        rating: parseInt(formData.rating),
        message: formData.message
    });
}

// Export functions
export {
    submitContactForm,
    submitInquiryForm,
    submitInternshipApplication,
    submitDeveloperApplication,
    submitJoinApplication,
    submitConsultationRequest,
    subscribeNewsletter,
    submitTestimonial
};
```

---

## Form Integration Examples

### 1. Contact Form Integration

**File**: `frontend/contact.html`

```html
<form id="contactForm">
    <input type="text" id="name" placeholder="Your Name" required>
    <input type="email" id="email" placeholder="Your Email" required>
    <input type="tel" id="phone" placeholder="Phone Number">
    <input type="text" id="subject" placeholder="Subject" required>
    <textarea id="message" placeholder="Your Message" required></textarea>
    <button type="submit">Send Message</button>
</form>

<script type="module">
    import { submitContactForm } from './api-client.js';

    const form = document.getElementById('contactForm');
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Show loading state
        const submitBtn = form.querySelector('button');
        submitBtn.disabled = true;
        submitBtn.textContent = 'Sending...';
        
        const formData = {
            name: document.getElementById('name').value,
            email: document.getElementById('email').value,
            phone: document.getElementById('phone').value,
            subject: document.getElementById('subject').value,
            message: document.getElementById('message').value
        };
        
        const result = await submitContactForm(formData);
        
        if (result.success) {
            alert('✓ Thank you! Your message has been sent successfully.');
            form.reset();
        } else {
            alert('✗ Error: ' + result.error);
        }
        
        // Reset button
        submitBtn.disabled = false;
        submitBtn.textContent = 'Send Message';
    });
</script>
```

### 2. Newsletter Subscription

**File**: `frontend/index.html`

```html
<form id="newsletterForm">
    <input type="email" id="newsletterEmail" placeholder="Enter your email" required>
    <button type="submit">Subscribe</button>
</form>

<script type="module">
    import { subscribeNewsletter } from './api-client.js';

    const form = document.getElementById('newsletterForm');
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const email = document.getElementById('newsletterEmail').value;
        const result = await subscribeNewsletter(email);
        
        if (result.success) {
            alert('✓ You have been subscribed to our newsletter!');
            form.reset();
        } else {
            alert('✗ ' + result.error);
        }
    });
</script>
```

### 3. Internship Application

**File**: `frontend/internship.html`

```html
<form id="internshipForm">
    <input type="text" id="fullName" placeholder="Full Name" required>
    <input type="email" id="email" placeholder="Email" required>
    <input type="tel" id="phone" placeholder="Phone Number" required>
    <input type="text" id="university" placeholder="University" required>
    <textarea id="skills" placeholder="Your Skills" required></textarea>
    <textarea id="experience" placeholder="Your Experience"></textarea>
    <input type="url" id="portfolioUrl" placeholder="Portfolio URL">
    <input type="url" id="resumeUrl" placeholder="Resume URL">
    <button type="submit">Apply Now</button>
</form>

<script type="module">
    import { submitInternshipApplication } from './api-client.js';

    const form = document.getElementById('internshipForm');
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = {
            fullName: document.getElementById('fullName').value,
            email: document.getElementById('email').value,
            phone: document.getElementById('phone').value,
            university: document.getElementById('university').value,
            skills: document.getElementById('skills').value,
            experience: document.getElementById('experience').value,
            portfolioUrl: document.getElementById('portfolioUrl').value,
            resumeUrl: document.getElementById('resumeUrl').value
        };
        
        const result = await submitInternshipApplication(formData);
        
        if (result.success) {
            alert('✓ Your application has been submitted successfully!');
            form.reset();
        } else {
            alert('✗ Error: ' + result.error);
        }
    });
</script>
```

---

## Advanced Patterns

### Loading State Management

```javascript
function showLoadingState(button) {
    button.disabled = true;
    button.setAttribute('data-original-text', button.textContent);
    button.textContent = 'Loading...';
}

function hideLoadingState(button) {
    button.disabled = false;
    button.textContent = button.getAttribute('data-original-text');
}
```

### Form Validation

```javascript
function validateContactForm(data) {
    const errors = [];
    
    if (!data.name || data.name.trim().length === 0) {
        errors.push('Name is required');
    }
    
    if (!data.email || !isValidEmail(data.email)) {
        errors.push('Valid email is required');
    }
    
    if (!data.message || data.message.trim().length < 10) {
        errors.push('Message must be at least 10 characters');
    }
    
    return errors;
}

function isValidEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}
```

### Error Handling with User Feedback

```javascript
async function submitFormWithErrorHandling(endpoint, data, onSuccess, onError) {
    try {
        // Validate data
        const errors = validateForm(data);
        if (errors.length > 0) {
            onError(errors.join(', '));
            return;
        }
        
        // Submit form
        const response = await fetch(`${API_BASE_URL}/${endpoint}/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Submission failed');
        }
        
        const result = await response.json();
        onSuccess(result);
        
    } catch (error) {
        onError(error.message);
        console.error('Form submission error:', error);
    }
}
```

### Progress Indication

```javascript
function uploadFileWithProgress(file) {
    return new Promise((resolve, reject) => {
        const formData = new FormData();
        formData.append('file', file);
        
        const xhr = new XMLHttpRequest();
        
        xhr.upload.addEventListener('progress', (event) => {
            if (event.lengthComputable) {
                const percentComplete = (event.loaded / event.total) * 100;
                console.log(`Upload progress: ${percentComplete.toFixed(2)}%`);
                // Update progress bar
            }
        });
        
        xhr.addEventListener('load', () => {
            if (xhr.status === 200) {
                resolve(JSON.parse(xhr.responseText));
            } else {
                reject(new Error('Upload failed'));
            }
        });
        
        xhr.addEventListener('error', () => reject(new Error('Upload error')));
        
        xhr.open('POST', `${API_BASE_URL}/upload/`);
        xhr.send(formData);
    });
}
```

---

## Environment Configuration

Create `frontend/config.js`:

```javascript
// Development
export const API_CONFIG = {
    development: {
        baseUrl: 'http://localhost:8000/api/forms'
    },
    production: {
        baseUrl: 'https://api.xstn.com/api/forms'
    }
};

export const getCurrentEnvironment = () => {
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        return 'development';
    }
    return 'production';
};

export const API_BASE_URL = API_CONFIG[getCurrentEnvironment()].baseUrl;
```

---

## CORS Configuration

Ensure your Django backend has CORS enabled for your frontend domain:

**In Django settings.py**:
```python
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'https://yourdomain.com'
]
```

---

## Testing API Endpoints

### Using fetch in Browser Console

```javascript
// Test contact form submission
fetch('http://localhost:8000/api/forms/contact-forms/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        name: 'Test User',
        email: 'test@example.com',
        phone: '+1234567890',
        subject: 'Test',
        message: 'This is a test'
    })
})
.then(response => response.json())
.then(data => console.log('Success:', data))
.catch(error => console.error('Error:', error));
```

### Using Postman

1. Create a new POST request
2. URL: `http://localhost:8000/api/forms/contact-forms/`
3. Headers: `Content-Type: application/json`
4. Body (raw JSON):
```json
{
    "name": "Test User",
    "email": "test@example.com",
    "phone": "+1234567890",
    "subject": "Test",
    "message": "This is a test message"
}
```

---

## Response Handling

### Success Response
```json
{
    "id": 1,
    "name": "Test User",
    "email": "test@example.com",
    "phone": "+1234567890",
    "subject": "Test",
    "message": "This is a test",
    "is_read": false,
    "created_at": "2024-01-15T10:30:00Z"
}
```

### Error Response
```json
{
    "error": "Validation error",
    "details": {
        "email": ["Enter a valid email address"],
        "name": ["This field may not be blank"]
    }
}
```

---

## Troubleshooting

### CORS Error
```
Access to XMLHttpRequest blocked by CORS policy
```
**Solution**: Check CORS_ALLOWED_ORIGINS in Django settings.py

### 404 Not Found
```
POST http://localhost:8000/api/forms/contact-forms/ 404
```
**Solution**: Verify API endpoint URL and ensure Django server is running

### Empty Response
```
Unexpected end of JSON input
```
**Solution**: Check API response with Network tab in DevTools; ensure backend is returning valid JSON

---

## Best Practices

1. **Always validate input** before sending to API
2. **Show loading state** during form submission
3. **Provide user feedback** (success/error messages)
4. **Use environment variables** for API URL
5. **Handle network errors** gracefully
6. **Sanitize user input** to prevent XSS
7. **Use HTTPS** in production
8. **Rate limiting** - implement on frontend if needed
9. **Test all endpoints** with Postman or curl
10. **Log API errors** for debugging

---

## API Endpoint Reference

| Form Type | Endpoint | Method |
|-----------|----------|--------|
| Contact | `/contact-forms/` | POST |
| Inquiry | `/inquiry-forms/` | POST |
| Internship | `/internship-applications/` | POST |
| Developer | `/developer-applications/` | POST |
| Join | `/join-applications/` | POST |
| Consultation | `/consultation-requests/` | POST |
| Newsletter | `/newsletter-subscriptions/` | POST |
| Testimonial | `/testimonials/` | POST |

---

## Next Steps

1. Import `api-client.js` into your forms
2. Test each form with the browser console
3. Update form submission handlers to use API functions
4. Test with Postman to verify endpoints
5. Deploy frontend and test with production backend

---

**Last Updated**: 2024
