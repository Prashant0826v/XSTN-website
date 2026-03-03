from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.contact import ContactFormCreate, ContactFormResponse, InquiryFormCreate, InquiryFormResponse
from app.schemas.internship import InternshipApplicationCreate, InternshipApplicationResponse
from app.services.form_service import (
    create_contact_form,
    create_inquiry_form,
    create_internship_application,
    get_contact_forms,
    get_inquiry_forms,
    get_internship_applications,
)
from app.services.email_service import send_contact_form_notification, send_confirmation_email

router = APIRouter(prefix="/api/forms", tags=["forms"])

@router.post("/contact", response_model=ContactFormResponse)
async def submit_contact_form(
    form_data: ContactFormCreate,
    db: Session = Depends(get_db)
):
    """Submit a contact form"""
    form = create_contact_form(db, form_data)
    
    # Send emails
    await send_contact_form_notification(
        form_data.name,
        form_data.email,
        form_data.subject,
        form_data.message
    )
    await send_confirmation_email(form_data.email, form_data.name)
    
    return form

@router.post("/inquiry", response_model=InquiryFormResponse)
async def submit_inquiry_form(
    form_data: InquiryFormCreate,
    db: Session = Depends(get_db)
):
    """Submit an inquiry form (Proposal request)"""
    form = create_inquiry_form(db, form_data)
    
    # Send emails
    await send_contact_form_notification(
        form_data.name,
        form_data.email,
        f"Project Inquiry - {form_data.project_type}",
        form_data.message
    )
    await send_confirmation_email(form_data.email, form_data.name)
    
    return form

@router.post("/internship", response_model=InternshipApplicationResponse)
async def submit_internship_application(
    app_data: InternshipApplicationCreate,
    db: Session = Depends(get_db)
):
    """Submit an internship application"""
    application = create_internship_application(db, app_data)
    
    # Send confirmation email
    await send_confirmation_email(app_data.email, app_data.full_name)
    
    return application

@router.get("/contact", response_model=list[ContactFormResponse])
async def get_contact_forms_list(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all contact forms (Admin only)"""
    return get_contact_forms(db, skip, limit)

@router.get("/inquiry", response_model=list[InquiryFormResponse])
async def get_inquiry_forms_list(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all inquiry forms (Admin only)"""
    return get_inquiry_forms(db, skip, limit)

@router.get("/internship", response_model=list[InternshipApplicationResponse])
async def get_internship_applications_list(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all internship applications (Admin only)"""
    return get_internship_applications(db, skip, limit)
