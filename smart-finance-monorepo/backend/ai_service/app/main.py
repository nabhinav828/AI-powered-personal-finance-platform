import sys
import os

# Path Hack for Shared library
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from uuid import UUID
from pydantic import BaseModel
from shared.database import database
from . import logic

app = FastAPI(title="SmartFinance AI Advisor")

# CORS (Allow Frontend)
origins = ["http://localhost:5173", "http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Schema
class AnalysisRequest(BaseModel):
    user_id: UUID

@app.post("/analyze")
def get_financial_advice(request: AnalysisRequest, db: Session = Depends(database.get_db)):
    try:
        advice = logic.analyze_finances(request.user_id, db)
        return {"advice": advice}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))