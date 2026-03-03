from sqlalchemy import Column, String, Text, DateTime, Integer, Boolean
from datetime import datetime
from app.core.database import Base

class InternshipApplication(Base):
    __tablename__ = "internship_applications"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False, index=True)
    phone = Column(String, nullable=False)
    university = Column(String, nullable=False)
    skills = Column(Text, nullable=False)
    experience = Column(Text, nullable=True)
    portfolio_url = Column(String, nullable=True)
    resume_url = Column(String, nullable=True)
    status = Column(String, default="pending", index=True)  # pending, reviewed, selected, rejected
    notes = Column(Text, nullable=True)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    def __repr__(self):
        return f"<InternshipApplication {self.email}>"
