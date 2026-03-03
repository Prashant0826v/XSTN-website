from pydantic import BaseModel, EmailStr
from datetime import datetime

class ContactFormCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str | None = None
    subject: str
    message: str

class ContactFormResponse(ContactFormCreate):
    id: int
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True

class InquiryFormCreate(BaseModel):
    name: str
    email: EmailStr
    company: str | None = None
    project_type: str
    budget_range: str | None = None
    timeline: str | None = None
    message: str

class InquiryFormResponse(InquiryFormCreate):
    id: int
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True
