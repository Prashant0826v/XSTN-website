# Frontend Email Verification Integration Guide

Complete guide for integrating email verification workflow on the frontend.

---

## Overview

The email verification workflow requires coordination between frontend and backend:

1. **Frontend**: Shows form submission UI
2. **Backend**: Sends verification email
3. **User**: Clicks email link
4. **Frontend**: Displays verification status
5. **Backend**: Sends admin notification

---

## Frontend Implementation

### Step 1: Form Submission

**When user submits a form on the website:**

```javascript
// Example: Contact form submission
async function submitContactForm(formData) {
  try {
    const response = await fetch('/api/contact/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        name: formData.name,
        email: formData.email,
        phone: formData.phone,
        subject: formData.subject,
        message: formData.message
      })
    });

    if (response.status === 201) {
      const data = await response.json();
      
      // Show success message
      showMessage(
        '✓ Form submitted! Check your email for verification link.',
        'success'
      );
      
      // Store form data for later (if needed)
      localStorage.setItem('pending_verification', JSON.stringify({
        submitted_at: new Date(),
        email: formData.email
      }));
      
      // Redirect to verification page
      redirectToVerificationPage();
    } else {
      showMessage('❌ Error submitting form. Please try again.', 'error');
    }
  } catch (error) {
    console.error('Form submission error:', error);
    showMessage('❌ Network error. Please check your connection.', 'error');
  }
}
```

### Step 2: Verification Page UI

**After form submission, show a verification message:**

```html
<div id="verification-container" class="verification-page">
  <div class="verification-box">
    <h2>📧 Verify Your Email</h2>
    
    <p class="info-text">
      We've sent a verification link to <strong id="user-email"></strong>
    </p>
    
    <div class="step-box">
      <div class="step-number">1</div>
      <p>Check your email inbox</p>
    </div>
    
    <div class="step-box">
      <div class="step-number">2</div>
      <p>Click the verification link</p>
    </div>
    
    <div class="step-box">
      <div class="step-number">3</div>
      <p>You'll see a confirmation message</p>
    </div>
    
    <p class="timer-text">⏱️ Verification link expires in 24 hours</p>
    
    <div id="verification-result" class="hidden">
      <!-- Will show success/failure here -->
    </div>
    
    <button onclick="requestNewToken()" class="btn-secondary">
      Didn't receive email? Request new link
    </button>
  </div>
</div>
```

### Step 3: Handle Verification Link Click

**User clicks link in email, which contains token in URL:**

```
Frontend URL format:
https://xstn.com/verify-email?type=contact&token=a1b2c3d4e5f6...

When page loads, extract token and form type:
```

```javascript
// On page load, check for verification token in URL
function handleVerificationPage() {
  const params = new URLSearchParams(window.location.search);
  const token = params.get('token');
  const formType = params.get('type');
  
  if (token && formType) {
    // Auto-verify when page loads
    verifyEmailToken(token, formType);
  }
}

// Call on page load
window.addEventListener('load', handleVerificationPage);
```

### Step 4: Send Token to Backend

**Verify token by calling backend endpoint:**

```javascript
async function verifyEmailToken(token, formType) {
  try {
    // Build endpoint based on form type
    const endpoints = {
      contact: '/api/contact/verify_email/',
      inquiry: '/api/inquiry/verify_email/',
      internship: '/api/internship/verify_email/',
      developer: '/api/developer/verify_email/',
      join: '/api/join/verify_email/',
      consultation: '/api/consultation/verify_email/',
      testimonial: '/api/testimonial/verify_email/'
    };
    
    const endpoint = endpoints[formType];
    
    if (!endpoint) {
      throw new Error('Invalid form type');
    }
    
    // Show loading state
    showVerificationLoading();
    
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ token: token })
    });
    
    if (response.status === 200) {
      const data = await response.json();
      showVerificationSuccess(data.message);
      
      // Clear stored data
      localStorage.removeItem('pending_verification');
      
      // Redirect after 3 seconds
      setTimeout(() => {
        window.location.href = '/thank-you.html';
      }, 3000);
    } else if (response.status === 400) {
      const data = await response.json();
      showVerificationError(data.error);
    }
  } catch (error) {
    console.error('Verification error:', error);
    showVerificationError('❌ Verification failed. Please try again.');
  }
}
```

### Step 5: UI Components

**Helper functions for UI display:**

```javascript
function showVerificationLoading() {
  const resultDiv = document.getElementById('verification-result');
  resultDiv.classList.remove('hidden');
  resultDiv.innerHTML = `
    <div class="loading">
      <div class="spinner"></div>
      <p>Verifying your email...</p>
    </div>
  `;
}

function showVerificationSuccess(message) {
  const resultDiv = document.getElementById('verification-result');
  resultDiv.classList.remove('hidden');
  resultDiv.innerHTML = `
    <div class="success-message">
      <div class="checkmark">✓</div>
      <h3>Verified Successfully!</h3>
      <p>${message}</p>
      <p class="redirect-text">Redirecting in 3 seconds...</p>
    </div>
  `;
}

function showVerificationError(error) {
  const resultDiv = document.getElementById('verification-result');
  resultDiv.classList.remove('hidden');
  resultDiv.innerHTML = `
    <div class="error-message">
      <div class="error-icon">✕</div>
      <h3>Verification Failed</h3>
      <p>${error}</p>
      <button onclick="requestNewToken()" class="btn-primary">
        Request new verification link
      </button>
    </div>
  `;
}

function showMessage(text, type) {
  // Create notification banner
  const banner = document.createElement('div');
  banner.className = `notification ${type}`;
  banner.textContent = text;
  document.body.appendChild(banner);
  
  // Auto-remove after 5 seconds
  setTimeout(() => banner.remove(), 5000);
}

function redirectToVerificationPage() {
  // Navigate to verification page
  window.location.href = '/verify-email.html';
}
```

### Step 6: Request New Token (If Link Expired)

**Allow user to request new verification link:**

```javascript
async function requestNewToken() {
  const email = document.getElementById('user-email').textContent;
  const formType = new URLSearchParams(window.location.search).get('type');
  
  try {
    // Re-submit the form with original data
    // This generates a new token
    
    showMessage('✓ New verification link sent to ' + email, 'success');
  } catch (error) {
    showMessage('❌ Error requesting new link. Please try again.', 'error');
  }
}
```

---

## HTML Templates

### Verification Page Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>XSTN - Email Verification</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <div class="navbar">
    <h1>XSTN</h1>
  </div>
  
  <div id="verification-container" class="verification-page">
    <div class="verification-box">
      <h2>📧 Verify Your Email</h2>
      
      <p class="info-text">
        We've sent a verification link to<br>
        <strong id="user-email" class="email-display">your@email.com</strong>
      </p>
      
      <div class="steps-container">
        <div class="step-box">
          <div class="step-number">1</div>
          <div class="step-content">
            <h4>Check Your Email</h4>
            <p>Look for the verification email from XSTN</p>
          </div>
        </div>
        
        <div class="step-box">
          <div class="step-number">2</div>
          <div class="step-content">
            <h4>Click The Link</h4>
            <p>Open the verification link in the email</p>
          </div>
        </div>
        
        <div class="step-box">
          <div class="step-number">3</div>
          <div class="step-content">
            <h4>Confirmed</h4>
            <p>You'll be automatically redirected</p>
          </div>
        </div>
      </div>
      
      <div class="timer">
        <p>⏱️ Verification link expires in 24 hours</p>
      </div>
      
      <div id="verification-result" class="hidden">
        <!-- Dynamic content inserted here -->
      </div>
      
      <div class="actions">
        <button onclick="requestNewToken()" class="btn-secondary">
          Didn't receive email?
        </button>
        <button onclick="window.location='/'" class="btn-outline">
          Go Back
        </button>
      </div>
      
      <p class="help-text">
        Check your spam folder if you don't see the email.
      </p>
    </div>
  </div>
  
  <script src="verify-email.js"></script>
</body>
</html>
```

### CSS for Verification Page

```css
.verification-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 80px);
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.verification-box {
  background: white;
  border-radius: 10px;
  padding: 40px;
  max-width: 500px;
  width: 100%;
  box-shadow: 0 10px 40px rgba(0,0,0,0.1);
}

.verification-box h2 {
  text-align: center;
  font-size: 24px;
  margin-bottom: 20px;
  color: #333;
}

.info-text {
  text-align: center;
  color: #666;
  margin-bottom: 30px;
}

.email-display {
  color: #667eea;
  word-break: break-all;
}

.steps-container {
  margin: 30px 0;
}

.step-box {
  display: flex;
  margin-bottom: 15px;
  padding: 15px;
  background: #f8f9ff;
  border-left: 4px solid #667eea;
  border-radius: 5px;
}

.step-number {
  min-width: 40px;
  height: 40px;
  background: #667eea;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  margin-right: 15px;
  flex-shrink: 0;
}

.step-content h4 {
  margin: 0 0 5px 0;
  color: #333;
}

.step-content p {
  margin: 0;
  color: #666;
  font-size: 14px;
}

.timer {
  text-align: center;
  color: #ff6b6b;
  margin: 20px 0;
  font-weight: 500;
}

.loading {
  text-align: center;
  padding: 30px;
}

.spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #667eea;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin: 0 auto 15px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.success-message {
  text-align: center;
  padding: 30px;
  background: #ecfdf5;
  border-radius: 5px;
  margin-bottom: 20px;
}

.checkmark {
  font-size: 48px;
  color: #10b981;
  margin-bottom: 10px;
}

.success-message h3 {
  color: #10b981;
  margin: 10px 0;
}

.success-message p {
  color: #666;
  margin: 5px 0;
}

.redirect-text {
  font-size: 12px;
  color: #999;
  margin-top: 10px !important;
}

.error-message {
  text-align: center;
  padding: 30px;
  background: #fef2f2;
  border-radius: 5px;
  margin-bottom: 20px;
}

.error-icon {
  font-size: 48px;
  color: #ef4444;
  margin-bottom: 10px;
}

.error-message h3 {
  color: #ef4444;
  margin: 10px 0;
}

.error-message p {
  color: #666;
  margin: 5px 0;
}

.actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.actions button {
  flex: 1;
  padding: 12px;
  border: none;
  border-radius: 5px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-secondary {
  background: #f3f4f6;
  color: #333;
}

.btn-secondary:hover {
  background: #e5e7eb;
}

.btn-outline {
  background: white;
  color: #667eea;
  border: 2px solid #667eea;
}

.btn-outline:hover {
  background: #f8f9ff;
}

.help-text {
  text-align: center;
  font-size: 12px;
  color: #999;
  margin-top: 15px;
}
```

---

## JavaScript for Verification

### verify-email.js

```javascript
// Extract email from storage and display
function displayUserEmail() {
  const stored = localStorage.getItem('pending_verification');
  if (stored) {
    const data = JSON.parse(stored);
    document.getElementById('user-email').textContent = data.email;
  }
}

// Handle page load
window.addEventListener('load', () => {
  displayUserEmail();
  handleVerificationPage();
});

// Main verification handler
function handleVerificationPage() {
  const params = new URLSearchParams(window.location.search);
  const token = params.get('token');
  const formType = params.get('type') || 'contact';
  
  if (token) {
    verifyEmailToken(token, formType);
  }
}

// Verify token with backend
async function verifyEmailToken(token, formType) {
  const endpoints = {
    contact: '/api/contact/verify_email/',
    inquiry: '/api/inquiry/verify_email/',
    internship: '/api/internship/verify_email/',
    developer: '/api/developer/verify_email/',
    join: '/api/join/verify_email/',
    consultation: '/api/consultation/verify_email/',
    testimonial: '/api/testimonial/verify_email/'
  };
  
  const endpoint = endpoints[formType];
  
  if (!endpoint) {
    showVerificationError('Invalid form type');
    return;
  }
  
  showVerificationLoading();
  
  try {
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ token: token })
    });
    
    const data = await response.json();
    
    if (response.status === 200) {
      showVerificationSuccess(data.message);
      localStorage.removeItem('pending_verification');
      
      setTimeout(() => {
        window.location.href = '/thank-you.html';
      }, 3000);
    } else {
      showVerificationError(data.error || 'Verification failed');
    }
  } catch (error) {
    console.error('Error:', error);
    showVerificationError('Network error. Please try again.');
  }
}

// UI Functions
function showVerificationLoading() {
  document.getElementById('verification-result').innerHTML = `
    <div class="loading">
      <div class="spinner"></div>
      <p>Verifying your email...</p>
    </div>
  `;
  document.getElementById('verification-result').classList.remove('hidden');
}

function showVerificationSuccess(message) {
  document.getElementById('verification-result').innerHTML = `
    <div class="success-message">
      <div class="checkmark">✓</div>
      <h3>Verified Successfully!</h3>
      <p>${message}</p>
      <p class="redirect-text">Redirecting in 3 seconds...</p>
    </div>
  `;
  document.getElementById('verification-result').classList.remove('hidden');
}

function showVerificationError(error) {
  document.getElementById('verification-result').innerHTML = `
    <div class="error-message">
      <div class="error-icon">✕</div>
      <h3>Verification Failed</h3>
      <p>${error}</p>
    </div>
  `;
  document.getElementById('verification-result').classList.remove('hidden');
}

function requestNewToken() {
  const stored = localStorage.getItem('pending_verification');
  if (stored) {
    const data = JSON.parse(stored);
    // Redirect back to form to re-submit
    window.location.href = '/contact.html?email=' + encodeURIComponent(data.email);
  } else {
    window.location.href = '/';
  }
}
```

---

## Integration Checklist

- [ ] Add form submission handler in contact.js/join.js/etc.
- [ ] Create verify-email.html page
- [ ] Add verify-email.js script
- [ ] Add CSS for verification UI
- [ ] Store pending verification in localStorage
- [ ] Display user email on verification page
- [ ] Extract token from URL query params
- [ ] Call verification endpoint with token
- [ ] Handle success/error responses
- [ ] Redirect on successful verification
- [ ] Test with all form types (contact, internship, etc.)
- [ ] Test token expiration (24 hours)
- [ ] Test requested new token flow

---

## Testing the Verification Flow

### Manual Testing:

```bash
# 1. Submit form
POST /api/contact/ with test email

# 2. Check email (or logs in development)
# Find verification token

# 3. Click verification link
GET /verify-email.html?type=contact&token=YOUR_TOKEN

# 4. Verify in admin dashboard
# Form should show is_verified: true
```

### Automated Testing:

```javascript
test('Email verification workflow', async () => {
  // 1. Submit form
  const submitResponse = await fetch('/api/contact/', {
    method: 'POST',
    body: JSON.stringify(testFormData)
  });
  
  // 2. Extract token
  const token = 'test-token-123';
  
  // 3. Verify email
  const verifyResponse = await fetch('/api/contact/verify_email/', {
    method: 'POST',
    body: JSON.stringify({ token })
  });
  
  expect(verifyResponse.status).toBe(200);
  expect(verifyResponse.json().verified).toBe(true);
});
```

---

**Guide Version**: 1.0  
**Last Updated**: 2024  
**Status**: ✅ Ready for Implementation
