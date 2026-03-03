# Email Configuration Guide

## Current Status
✅ Email system is configured to work in **DEVELOPMENT MODE** (emails print to terminal/console)

## How It Works

### Development Mode (Current)
- Emails are printed to the server terminal instead of being sent
- Perfect for testing form submissions locally
- You'll see confirmation emails in the Django server console

### Production Mode (When Ready)
To enable actual email sending via SMTP, follow these steps:

## Setup Gmail for Email Sending

### Step 1: Enable 2-Factor Authentication
1. Go to https://myaccount.google.com
2. Click "Security" in the menu
3. Enable 2-Step Verification

### Step 2: Generate App Password
1. After enabling 2FA, go to https://myaccount.google.com/apppasswords
2. Select "Mail" and "Windows Computer" (or your device)
3. Google will generate a 16-character password
4. Copy this password

### Step 3: Update .env File
Create a `.env` file in the backend folder with:
```
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-16-char-app-password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
FROM_EMAIL=your-email@gmail.com
```

### Step 4: Restart Django Server
Kill the server and restart it. Now emails will be sent via Gmail.

## Email Templates Currently Supported

1. **Contact Form Confirmation**
   - Sent when user submits contact form
   - Auto-reply confirming receipt

2. **Proposal Inquiry Confirmation**
   - Sent when user submits proposal request
   - Includes 48-hour response timeline

3. **Internship Application Confirmation**
   - Sent when user applies for internship
   - Includes review timeline

4. **Developer Application Confirmation**
   - Sent when user applies to join as developer
   - Includes 3-5 business day timeline

## Test Emails Right Now

All forms are functional! When you submit a form:
1. Check the **Django server console** - you'll see the email text there
2. The form submission is saved in admin panel
3. Admin at: http://localhost:8000/admin/forms/

## For Production Deployment
- Update settings.py to use your email provider
- Never commit real credentials to git
- Always use environment variables or secrets manager
- Test email sending before going live

---

**Current Email Backend:** Console (Development)  
**Status:** ✅ Ready for testing  
**When Production Credentials Added:** Emails will be sent automatically
