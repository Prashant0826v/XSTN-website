from pydantic import BaseModel, EmailStr
from datetime import datetime

class InternshipApplicationCreate(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    university: str
    skills: str
    experience: str | None = None
    portfolio_url: str | None = None
    resume_url: str | None = None

class InternshipApplicationResponse(InternshipApplicationCreate):
    id: int
    status: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True
