import sys
import os

# --- PATH HACK (To find 'shared' folder) ---
# This adds the project root to Python's path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from shared.database import models, database
from . import schemas, crud # Note the underscore in core_service if folder name has dash, but Python imports usually prefer underscores. 
# actually, let's fix the import path issue cleanly below.

app = FastAPI(title="SmartFinance Core API")

# --- NEW: ADD CORS MIDDLEWARE ---
origins = [
    "http://localhost:3000",
    "http://localhost:5173", # Vite default port
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --------------------------------

# Dependency to get DB session
get_db = database.get_db

# Create Tables (if they don't exist)
models.Base.metadata.create_all(bind=database.engine)

@app.get("/")
def read_root():
    return {"message": "SmartFinance Core Service is Running!"}

# --- USER ENDPOINTS ---
@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

# --- TRANSACTION ENDPOINTS ---
@app.post("/transactions/", response_model=schemas.TransactionResponse)
def create_transaction(
    transaction: schemas.TransactionCreate, 
    user_id: UUID, # In real app, we get this from Auth Token. For now, manual input.
    db: Session = Depends(get_db)
):
    return crud.create_transaction(db=db, transaction=transaction, user_id=user_id)

@app.get("/transactions/{user_id}", response_model=List[schemas.TransactionResponse])
def read_transactions(user_id: UUID, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    transactions = crud.get_transactions(db, user_id=user_id, skip=skip, limit=limit)
    return transactions