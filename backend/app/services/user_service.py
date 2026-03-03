from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash

def create_user(db: Session, user_create: UserCreate) -> User:
    """Create a new user"""
    db_user = User(
        email=user_create.email,
        hashed_password=get_password_hash(user_create.password),
        full_name=user_create.full_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str) -> User | None:
    """Get user by email"""
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: int) -> User | None:
    """Get user by ID"""
    return db.query(User).filter(User.id == user_id).first()

def user_exists(db: Session, email: str) -> bool:
    """Check if user exists"""
    return db.query(User).filter(User.email == email).first() is not None
