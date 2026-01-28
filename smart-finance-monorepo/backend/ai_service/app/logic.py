import os
from langchain_google_genai import ChatGoogleGenerativeAI
from sqlalchemy.orm import Session
from shared.database import models
from uuid import UUID

# Initialize the AI Model
llm = ChatGoogleGenerativeAI(
    model="gemini-flash-latest",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.7
)

def analyze_finances(user_id: UUID, db: Session):
    # 1. Fetch Data
    transactions = db.query(models.Transaction).filter(models.Transaction.user_id == user_id).all()
    debts = db.query(models.Debt).filter(models.Debt.user_id == user_id).all()

    # 2. Summarize Data for the AI (Save tokens)
    total_income = sum(t.amount for t in transactions if t.type == 'income')
    total_expense = sum(t.amount for t in transactions if t.type == 'expense')
    
    # Group expenses by category (Simple version)
    # Note: In a real app, you'd use SQL Group By for speed.
    category_summary = {}
    for t in transactions:
        if t.type == 'expense':
            cat_name = t.description # Using description as category for now since categories are optional
            category_summary[cat_name] = category_summary.get(cat_name, 0) + float(t.amount)

    # 3. Construct the Prompt
    prompt = f"""
    You are a brutal but helpful financial planner. Analyze this user's monthly snapshot:
    
    - Total Income: ${total_income}
    - Total Spent: ${total_expense}
    - Savings Rate: {((total_income - total_expense)/total_income)*100 if total_income > 0 else 0}%
    - Top Expenses: {category_summary}
    - Debts: {[d.name for d in debts]}

    Task:
    1. Identify 1 bad spending habit.
    2. Give 1 specific action to save money next week.
    3. If they have debt, recommend a payoff strategy.
    
    Keep it short (under 100 words).
    """

    # 4. Call AI
    response = llm.invoke(prompt)
    return response.content