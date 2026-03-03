"""
XSTN Email Service - Comprehensive Email Notification System
Handles email notifications and verification for form submissions
"""

from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.urls import reverse
import logging

logger = logging.getLogger(__name__)


class EmailService:
    """
    Centralized email service for all form submissions and notifications
    """
    
    @staticmethod
    def get_company_email():
        """Get company email from settings"""
        return settings.DEFAULT_FROM_EMAIL
    
    @staticmethod
    def get_verification_link(token, form_type):
        """
        Generate verification link for email confirmation
        form_type: 'contact', 'inquiry', 'internship', 'developer', 'join', 'consultation'
        """
        # This will be your frontend URL
        frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')
        return f"{frontend_url}/verify-form?token={token}&type={form_type}"
    
    @staticmethod
    def send_verification_email(user_email, verification_link, form_type, user_name):
        """
        Send verification email to user
        User must click the link to verify they own the email
        """
        subject = "XSTN - Verify Your Email Address 🔐"
        
        html_message = f"""
        <html>
            <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
                <center>
                    <div style="
                        background-color: white; 
                        padding: 40px; 
                        border-radius: 8px; 
                        max-width: 600px;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                    ">
                        <h1 style="color: #38bdf8;">XSTN - Email Verification</h1>
                        <p style="color: #333; font-size: 16px;">Hi <strong>{user_name}</strong>,</p>
                        <p style="color: #666; line-height: 1.6;">
                            Thank you for submitting a form to XSTN! 
                            To confirm that this email address belongs to you, 
                            please click the verification link below:
                        </p>
                        
                        <a href="{verification_link}" style="
                            background-color: #38bdf8;
                            color: white;
                            padding: 12px 30px;
                            text-decoration: none;
                            border-radius: 5px;
                            display: inline-block;
                            margin: 20px 0;
                            font-weight: bold;
                        ">
                            Verify Email Address ✓
                        </a>
                        
                        <p style="color: #999; font-size: 12px; margin-top: 30px;">
                            <strong>Note:</strong> This link will expire in 24 hours.<br>
                            Form Type: <strong>{form_type.title()}</strong>
                        </p>
                        
                        <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                        
                        <p style="color: #666; font-size: 14px;">
                            If you didn't submit this form or received this email in error, 
                            please ignore it.
                        </p>
                        
                        <p style="color: #38bdf8; margin-top: 30px;">
                            Best regards,<br><strong>XSTN Team</strong>
                        </p>
                    </div>
                </center>
            </body>
        </html>
        """
        
        plain_message = f"""
        XSTN - Email Verification
        
        Hi {user_name},
        
        Thank you for submitting a form to XSTN! 
        To confirm that this email address belongs to you, 
        please click the verification link below:
        
        {verification_link}
        
        This link will expire in 24 hours.
        
        If you didn't submit this form, please ignore this email.
        
        Best regards,
        XSTN Team
        """
        
        try:
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=EmailService.get_company_email(),
                recipient_list=[user_email],
                html_message=html_message,
                fail_silently=False,
            )
            logger.info(f"Verification email sent to {user_email}")
            return True
        except Exception as e:
            logger.error(f"Failed to send verification email to {user_email}: {str(e)}")
            return False
    
    @staticmethod
    def send_admin_notification(form_data, form_type):
        """
        Send notification to admin/company email about new form submission
        """
        subject = f"🔔 XSTN - New {form_type.title()} Submission Received"
        company_email = EmailService.get_company_email()
        
        html_message = f"""
        <html>
            <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
                <center>
                    <div style="
                        background-color: white; 
                        padding: 40px; 
                        border-radius: 8px; 
                        max-width: 700px;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                    ">
                        <h1 style="color: #8b5cf6;">New {form_type.title()} Received</h1>
                        <p style="color: #666; font-size: 16px;">A new submission from a potential {form_type} has been received:</p>
                        
                        <div style="
                            background-color: #f9fafb; 
                            padding: 20px; 
                            border-radius: 5px; 
                            margin: 20px 0;
                            border-left: 4px solid #8b5cf6;
                        ">
                            {EmailService._format_form_data_html(form_data)}
                        </div>
                        
                        <div style="
                            background-color: #ecf0f1; 
                            padding: 15px; 
                            border-radius: 5px; 
                            margin: 20px 0;
                        ">
                            <strong style="color: #333;">⏰ Submitted At:</strong> 
                            <span style="color: #666;">{form_data.get('created_at', 'N/A')}</span><br>
                            <strong style="color: #333;">✉️ Email:</strong> 
                            <span style="color: #666;">{form_data.get('email', 'N/A')}</span>
                        </div>
                        
                        <a href="http://localhost:8000/admin/" style="
                            background-color: #8b5cf6;
                            color: white;
                            padding: 12px 30px;
                            text-decoration: none;
                            border-radius: 5px;
                            display: inline-block;
                            margin: 20px 0;
                            font-weight: bold;
                        ">
                            View in Admin Dashboard →
                        </a>
                        
                        <p style="color: #999; font-size: 12px; margin-top: 30px;">
                            This is an automated notification. Please don't reply to this email.
                        </p>
                    </div>
                </center>
            </body>
        </html>
        """
        
        plain_message = f"""
        New {form_type.title()} Received
        
        A new submission from a potential {form_type} has been received:
        
        {EmailService._format_form_data_plain(form_data)}
        
        Submitted At: {form_data.get('created_at', 'N/A')}
        Email: {form_data.get('email', 'N/A')}
        
        View in Admin Dashboard: http://localhost:8000/admin/
        
        This is an automated notification. Please don't reply to this email.
        """
        
        try:
            send_mail(
                subject=subject,
                message=plain_message,
                from_email="noreply@xstn.com",
                recipient_list=[company_email],
                html_message=html_message,
                fail_silently=False,
            )
            logger.info(f"Admin notification sent for new {form_type}")
            return True
        except Exception as e:
            logger.error(f"Failed to send admin notification: {str(e)}")
            return False
    
    @staticmethod
    def send_confirmation_email(user_email, user_name, form_type):
        """
        Send confirmation email to user after successful form verification
        """
        subject = f"XSTN - Your {form_type.title()} Has Been Verified ✓"
        
        html_message = f"""
        <html>
            <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
                <center>
                    <div style="
                        background-color: white; 
                        padding: 40px; 
                        border-radius: 8px; 
                        max-width: 600px;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                    ">
                        <h1 style="color: #10b981;">✓ Email Verified Successfully!</h1>
                        <p style="color: #333; font-size: 16px;">Hi <strong>{user_name}</strong>,</p>
                        <p style="color: #666; line-height: 1.6;">
                            Great news! Your email has been successfully verified. 
                            Your {form_type} submission has been confirmed and received by our team.
                        </p>
                        
                        <div style="
                            background-color: #ecfdf5; 
                            padding: 20px; 
                            border-radius: 5px; 
                            margin: 20px 0;
                            border-left: 4px solid #10b981;
                        ">
                            <p style="color: #047857; font-weight: bold;">✓ What happens next?</p>
                            <ul style="color: #666; text-align: left;">
                                <li>Our team will review your submission</li>
                                <li>You'll receive updates via email</li>
                                <li>We typically respond within 24-48 hours</li>
                            </ul>
                        </div>
                        
                        <p style="color: #666; margin-top: 20px;">
                            If you have any questions, feel free to reach out to us at 
                            <strong>{EmailService.get_company_email()}</strong>
                        </p>
                        
                        <p style="color: #38bdf8; margin-top: 30px;">
                            Best regards,<br><strong>XSTN Team</strong>
                        </p>
                    </div>
                </center>
            </body>
        </html>
        """
        
        plain_message = f"""
        Email Verified Successfully!
        
        Hi {user_name},
        
        Great news! Your email has been successfully verified. 
        Your {form_type} submission has been confirmed and received by our team.
        
        What happens next?
        - Our team will review your submission
        - You'll receive updates via email
        - We typically respond within 24-48 hours
        
        If you have any questions, feel free to reach out to us at {EmailService.get_company_email()}
        
        Best regards,
        XSTN Team
        """
        
        try:
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=EmailService.get_company_email(),
                recipient_list=[user_email],
                html_message=html_message,
                fail_silently=False,
            )
            logger.info(f"Confirmation email sent to {user_email}")
            return True
        except Exception as e:
            logger.error(f"Failed to send confirmation email to {user_email}: {str(e)}")
            return False
    
    @staticmethod
    def send_rejection_email(user_email, user_name, form_type, reason=""):
        """
        Send rejection email to user
        """
        subject = f"XSTN - Update on Your {form_type.title()} Submission"
        
        html_message = f"""
        <html>
            <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
                <center>
                    <div style="
                        background-color: white; 
                        padding: 40px; 
                        border-radius: 8px; 
                        max-width: 600px;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                    ">
                        <h1 style="color: #ef4444;">Application Review Complete</h1>
                        <p style="color: #333; font-size: 16px;">Hi <strong>{user_name}</strong>,</p>
                        <p style="color: #666; line-height: 1.6;">
                            Thank you for your interest in XSTN. 
                            We have completed our review of your {form_type} submission.
                        </p>
                        
                        <div style="
                            background-color: #fef2f2; 
                            padding: 20px; 
                            border-radius: 5px; 
                            margin: 20px 0;
                            border-left: 4px solid #ef4444;
                        ">
                            <p style="color: #991b1b; font-weight: bold;">Unfortunately, we have decided to move forward with other candidates at this time.</p>
                            {f'<p style="color: #dc2626; margin-top: 10px;"><strong>Feedback:</strong> {reason}</p>' if reason else ''}
                        </div>
                        
                        <p style="color: #666; margin-top: 20px;">
                            We appreciate your application and encourage you to apply again in the future. 
                            Don't hesitate to reach out if you have any questions.
                        </p>
                        
                        <p style="color: #38bdf8; margin-top: 30px;">
                            Best regards,<br><strong>XSTN Team</strong>
                        </p>
                    </div>
                </center>
            </body>
        </html>
        """
        
        plain_message = f"""
        Application Review Complete
        
        Hi {user_name},
        
        Thank you for your interest in XSTN. 
        We have completed our review of your {form_type} submission.
        
        Unfortunately, we have decided to move forward with other candidates at this time.
        {f'Feedback: {reason}' if reason else ''}
        
        We appreciate your application and encourage you to apply again in the future. 
        Don't hesitate to reach out if you have any questions.
        
        Best regards,
        XSTN Team
        """
        
        try:
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=EmailService.get_company_email(),
                recipient_list=[user_email],
                html_message=html_message,
                fail_silently=False,
            )
            logger.info(f"Rejection email sent to {user_email}")
            return True
        except Exception as e:
            logger.error(f"Failed to send rejection email to {user_email}: {str(e)}")
            return False
    
    @staticmethod
    def send_approval_email(user_email, user_name, form_type, next_steps=""):
        """
        Send approval/acceptance email to user
        """
        subject = f"🎉 XSTN - You've Been Selected! {form_type.title()}"
        
        html_message = f"""
        <html>
            <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
                <center>
                    <div style="
                        background-color: white; 
                        padding: 40px; 
                        border-radius: 8px; 
                        max-width: 600px;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                    ">
                        <h1 style="color: #10b981;">🎉 Congratulations {user_name}!</h1>
                        <p style="color: #333; font-size: 16px;">You've been selected!</p>
                        <p style="color: #666; line-height: 1.6;">
                            We're excited to let you know that your {form_type} submission has been approved. 
                            You're now part of the XSTN community!
                        </p>
                        
                        <div style="
                            background-color: #ecfdf5; 
                            padding: 20px; 
                            border-radius: 5px; 
                            margin: 20px 0;
                            border-left: 4px solid #10b981;
                        ">
                            <p style="color: #047857; font-weight: bold;">📋 Next Steps:</p>
                            {f'<p style="color: #666;">{next_steps}</p>' if next_steps else '<p style="color: #666;">Our team will contact you shortly with more details about your onboarding.</p>'}
                        </div>
                        
                        <p style="color: #666; margin-top: 20px;">
                            Welcome aboard! We're looking forward to working with you.
                        </p>
                        
                        <p style="color: #38bdf8; margin-top: 30px;">
                            Best regards,<br><strong>XSTN Team</strong>
                        </p>
                    </div>
                </center>
            </body>
        </html>
        """
        
        plain_message = f"""
        Congratulations {user_name}!
        
        You've been selected!
        
        We're excited to let you know that your {form_type} submission has been approved. 
        You're now part of the XSTN community!
        
        Next Steps:
        {next_steps if next_steps else 'Our team will contact you shortly with more details about your onboarding.'}
        
        Welcome aboard! We're looking forward to working with you.
        
        Best regards,
        XSTN Team
        """
        
        try:
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=EmailService.get_company_email(),
                recipient_list=[user_email],
                html_message=html_message,
                fail_silently=False,
            )
            logger.info(f"Approval email sent to {user_email}")
            return True
        except Exception as e:
            logger.error(f"Failed to send approval email to {user_email}: {str(e)}")
            return False
    
    @staticmethod
    def _format_form_data_html(form_data):
        """Format form data as HTML for email"""
        html = ""
        for key, value in form_data.items():
            if key not in ['id', 'created_at', 'is_read', 'is_verified', 'verification_token', 
                          'verification_token_created_at', 'verified_at']:
                label = key.replace('_', ' ').title()
                if isinstance(value, bool):
                    value = "Yes" if value else "No"
                html += f"<strong>{label}:</strong> {value}<br>"
        return html
    
    @staticmethod
    def _format_form_data_plain(form_data):
        """Format form data as plain text for email"""
        text = ""
        for key, value in form_data.items():
            if key not in ['id', 'created_at', 'is_read', 'is_verified', 'verification_token',
                          'verification_token_created_at', 'verified_at']:
                label = key.replace('_', ' ').title()
                if isinstance(value, bool):
                    value = "Yes" if value else "No"
                text += f"{label}: {value}\n"
        return text


# Convenience functions
def send_verification_email(email, token, form_type, name):
    """Convenience function to send verification email"""
    verification_link = EmailService.get_verification_link(token, form_type)
    return EmailService.send_verification_email(email, verification_link, form_type, name)


def send_admin_notification(form_data, form_type):
    """Convenience function to send admin notification"""
    return EmailService.send_admin_notification(form_data, form_type)


def send_confirmation_email(email, name, form_type):
    """Convenience function to send confirmation email"""
    return EmailService.send_confirmation_email(email, name, form_type)


def send_rejection_email(email, name, form_type, reason=""):
    """Convenience function to send rejection email"""
    return EmailService.send_rejection_email(email, name, form_type, reason)


def send_approval_email(email, name, form_type, next_steps=""):
    """Convenience function to send approval email"""
    return EmailService.send_approval_email(email, name, form_type, next_steps)
