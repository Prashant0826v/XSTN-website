from sqlalchemy import Column, String, Text, DateTime, Integer, Boolean
from datetime import datetime
from app.core.database import Base

class ContactForm(Base):
    __tablename__ = "contact_forms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, index=True)
    phone = Column(String, nullable=True)
    subject = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    def __repr__(self):
        return f"<ContactForm {self.email}>"

class InquiryForm(Base):
    __tablename__ = "inquiry_forms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, index=True)
    company = Column(String, nullable=True)
    project_type = Column(String, nullable=False)
    budget_range = Column(String, nullable=True)
    timeline = Column(String, nullable=True)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    def __repr__(self):
        return f"<InquiryForm {self.email}>"
