# shared/database/models.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Numeric, Date, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    transactions = relationship("Transaction", back_populates="user")
    debts = relationship("Debt", back_populates="user")

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    name = Column(String, nullable=False)
    is_system = Column(Boolean, default=False)

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    
    amount = Column(Numeric(10, 2), nullable=False)
    description = Column(Text, nullable=True)
    date = Column(Date, nullable=False)
    type = Column(String, nullable=False) # 'income' or 'expense'
    
    user = relationship("User", back_populates="transactions")
    category = relationship("Category")

class Debt(Base):
    __tablename__ = "debts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    name = Column(String, nullable=False)
    current_balance = Column(Numeric(10, 2), nullable=False)
    apr = Column(Numeric(5, 2), nullable=False)
    min_payment = Column(Numeric(10, 2), default=0)

    user = relationship("User", back_populates="debts")