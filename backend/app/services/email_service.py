import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

async def send_email(
    to_email: str,
    subject: str,
    body: str,
    is_html: bool = True
) -> bool:
    """Send email using SMTP"""
    try:
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = settings.FROM_EMAIL
        message["To"] = to_email

        mime_type = "html" if is_html else "plain"
        message.attach(MIMEText(body, mime_type))

        async with aiosmtplib.SMTP(hostname=settings.SMTP_SERVER, port=settings.SMTP_PORT) as smtp:
            await smtp.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            await smtp.send_message(message)
        
        logger.info(f"Email sent successfully to {to_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {str(e)}")
        return False

async def send_contact_form_notification(name: str, email: str, subject: str, message: str) -> bool:
    """Send contact form notification"""
    body = f"""
    <html>
        <body style="font-family: Arial, sans-serif;">
            <h2>New Contact Form Submission</h2>
            <p><strong>Name:</strong> {name}</p>
            <p><strong>Email:</strong> {email}</p>
            <p><strong>Subject:</strong> {subject}</p>
            <p><strong>Message:</strong></p>
            <p>{message}</p>
        </body>
    </html>
    """
    return await send_email(settings.FROM_EMAIL, f"New Contact: {subject}", body)

async def send_confirmation_email(email: str, name: str) -> bool:
    """Send confirmation email to user"""
    body = f"""
    <html>
        <body style="font-family: Arial, sans-serif;">
            <h2>Thank you for contacting XSTN</h2>
            <p>Hi {name},</p>
            <p>We have received your message and will get back to you shortly.</p>
            <p>Best regards,<br>XSTN Team</p>
        </body>
    </html>
    """
    return await send_email(email, "XSTN - We received your message", body)
