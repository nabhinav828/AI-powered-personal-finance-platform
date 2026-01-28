from pydantic import BaseModel
from datetime import date
from typing import Optional, List
from uuid import UUID

# 1. Base Schema (Shared properties)
class TransactionBase(BaseModel):
    amount: float
    description: Optional[str] = None
    date: date
    type: str  # 'income' or 'expense'
    category_id: Optional[int] = None

# 2. Create Schema (What the user sends to us)
class TransactionCreate(TransactionBase):
    pass

# 3. Response Schema (What we send back to the user)
# We add 'id' and 'user_id' because the DB generates those, not the user.
class TransactionResponse(TransactionBase):
    id: UUID
    user_id: UUID

    class Config:
        from_attributes = True  # Allows Pydantic to read SQLAlchemy models

# 4. User Schema (Simple version)
class UserCreate(BaseModel):
    email: str

class UserResponse(BaseModel):
    id: UUID
    email: str
    
    class Config:
        from_attributes = True