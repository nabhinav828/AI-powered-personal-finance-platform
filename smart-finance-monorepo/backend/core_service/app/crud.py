from sqlalchemy.orm import Session
from shared.database import models
from . import schemas
from uuid import UUID

# --- User Logic ---
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- Transaction Logic ---
def get_transactions(db: Session, user_id: UUID, skip: int = 0, limit: int = 100):
    return db.query(models.Transaction)\
             .filter(models.Transaction.user_id == user_id)\
             .offset(skip).limit(limit).all()

def create_transaction(db: Session, transaction: schemas.TransactionCreate, user_id: UUID):
    db_transaction = models.Transaction(**transaction.dict(), user_id=user_id)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction