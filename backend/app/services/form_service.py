from sqlalchemy.orm import Session
from app.models.contact import ContactForm, InquiryForm
from app.models.internship import InternshipApplication
from app.schemas.contact import ContactFormCreate, InquiryFormCreate
from app.schemas.internship import InternshipApplicationCreate

def create_contact_form(db: Session, form_data: ContactFormCreate) -> ContactForm:
    """Create a new contact form submission"""
    db_form = ContactForm(**form_data.dict())
    db.add(db_form)
    db.commit()
    db.refresh(db_form)
    return db_form

def create_inquiry_form(db: Session, form_data: InquiryFormCreate) -> InquiryForm:
    """Create a new inquiry form submission"""
    db_form = InquiryForm(**form_data.dict())
    db.add(db_form)
    db.commit()
    db.refresh(db_form)
    return db_form

def create_internship_application(db: Session, app_data: InternshipApplicationCreate) -> InternshipApplication:
    """Create a new internship application"""
    db_app = InternshipApplication(**app_data.dict())
    db.add(db_app)
    db.commit()
    db.refresh(db_app)
    return db_app

def get_contact_forms(db: Session, skip: int = 0, limit: int = 100):
    """Get all contact forms"""
    return db.query(ContactForm).offset(skip).limit(limit).all()

def get_inquiry_forms(db: Session, skip: int = 0, limit: int = 100):
    """Get all inquiry forms"""
    return db.query(InquiryForm).offset(skip).limit(limit).all()

def get_internship_applications(db: Session, skip: int = 0, limit: int = 100):
    """Get all internship applications"""
    return db.query(InternshipApplication).offset(skip).limit(limit).all()
