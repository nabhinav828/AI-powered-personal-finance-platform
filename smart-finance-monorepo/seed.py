import sys
import os
import random
from datetime import datetime, timedelta

# --- 1. Setup Environment to talk to Database ---
# Add the current directory to Python path so we can find 'shared'
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from sqlalchemy.orm import Session
from shared.database import models, database

# Initialize Database connection
db = database.SessionLocal()

def seed_data():
    print("🌱 Starting Database Seeding...")

    # --- 2. Create a Demo User ---
    email = "demo@smartfinance.com"
    user = db.query(models.User).filter(models.User.email == email).first()
    
    if not user:
        print(f"Creating user: {email}")
        user = models.User(email=email)
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        print(f"User {email} already exists. Using existing ID.")

    user_id = user.id
    print(f"✅ User ID: {user_id}")

    # --- 3. Create Categories ---
    # We check if they exist first to avoid duplicates
    category_names = ["Rent", "Groceries", "Dining Out", "Utilities", "Entertainment", "Transport", "Salary"]
    categories = {} # Map name -> ID

    for name in category_names:
        cat = db.query(models.Category).filter(models.Category.name == name).first()
        if not cat:
            cat = models.Category(name=name, is_system=True)
            db.add(cat)
            db.commit()
            db.refresh(cat)
        categories[name] = cat.id
    
    print("✅ Categories ensured.")

    # --- 4. Generate 3 Months of Transactions ---
    # Clear old transactions for this user to keep it clean (Optional)
    db.query(models.Transaction).filter(models.Transaction.user_id == user_id).delete()
    db.commit()

    transactions = []
    start_date = datetime.now() - timedelta(days=90) # Start 3 months ago

    # A. Fixed Monthly Bills (Rent, Internet)
    for i in range(3): # For each of the last 3 months
        month_date = start_date + timedelta(days=i*30)
        
        # Salary (2x a month)
        transactions.append(models.Transaction(
            user_id=user_id, category_id=categories["Salary"], amount=2500, 
            description="Bi-weekly Paycheck", date=month_date, type="income"
        ))
        transactions.append(models.Transaction(
            user_id=user_id, category_id=categories["Salary"], amount=2500, 
            description="Bi-weekly Paycheck", date=month_date + timedelta(days=15), type="income"
        ))

        # Rent
        transactions.append(models.Transaction(
            user_id=user_id, category_id=categories["Rent"], amount=1500, 
            description="Apartment Rent", date=month_date, type="expense"
        ))
        
        # Utilities
        transactions.append(models.Transaction(
            user_id=user_id, category_id=categories["Utilities"], amount=120.50, 
            description="Electric Bill", date=month_date + timedelta(days=5), type="expense"
        ))

    # B. Random Daily Spending (Coffee, Food, Uber)
    merchants = [
        ("Starbucks", 6.50, "Dining Out"),
        ("Chipotle", 14.20, "Dining Out"),
        ("Uber", 25.00, "Transport"),
        ("Netflix", 15.99, "Entertainment"),
        ("Kroger", 85.00, "Groceries"),
        ("Whole Foods", 120.00, "Groceries"),
        ("Shell Station", 45.00, "Transport"),
        ("Cinema AMC", 30.00, "Entertainment"),
    ]

    # Generate 40 random transactions
    for _ in range(40):
        merchant, avg_cost, cat_name = random.choice(merchants)
        # Randomize price slightly (e.g., $6.50 -> $6.82)
        price = round(avg_cost * random.uniform(0.8, 1.2), 2)
        # Random date in last 90 days
        tx_date = start_date + timedelta(days=random.randint(0, 90))
        
        transactions.append(models.Transaction(
            user_id=user_id, 
            category_id=categories[cat_name], 
            amount=price, 
            description=merchant, 
            date=tx_date, 
            type="expense"
        ))

    db.add_all(transactions)
    db.commit()
    print(f"✅ Inserted {len(transactions)} realistic transactions.")

    # --- 5. Add Debt (The Problem Area) ---
    # Check if debt exists
    existing_debt = db.query(models.Debt).filter(models.Debt.user_id == user_id).first()
    if not existing_debt:
        debt = models.Debt(
            user_id=user_id,
            name="Chase Sapphire Reserve",
            current_balance=4500.00, # High balance
            apr=22.99, # High interest
            min_payment=150.00
        )
        db.add(debt)
        db.commit()
        print("✅ Added Credit Card Debt record.")
    else:
        print("Debt record already exists.")

    print("\n🎉 Database populated successfully!")
    print(f"👉 Use this User ID in your frontend: {user_id}")

if __name__ == "__main__":
    seed_data()