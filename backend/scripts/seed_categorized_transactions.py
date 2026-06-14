import os
import sys
from datetime import datetime, timezone, timedelta
import random

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.extensions import db
from app.models import Category, Transaction

# Seed data mapping keywords to categories
MERCHANTS = {
    "Food & Dining": ["SWIGGY ORDER", "ZOMATO DINING", "MCDONALDS", "KFC", "DOMINOS PIZZA", "STARBUCKS", "CAFE COFFEE DAY", "LOCAL BAKERY", "UBER EATS"],
    "Transport": ["UBER TRIP", "OLA RIDE", "METRO RECHARGE", "PETROL BUMP", "INDIAN OIL", "RAPIDO BIKE", "FLIGHT TICKET", "TRAIN IRCTC"],
    "Utilities": ["ELECTRICITY BILL", "WATER BILL", "JIO RECHARGE", "AIRTEL BROADBAND", "GAS CYLINDER", "MUNICIPAL TAX"],
    "Healthcare": ["APOLLO PHARMACY", "HOSPITAL VISIT", "CLINIC CONSULTATION", "MEDPLUS", "LAB TEST", "HEALTH INSURANCE PREMIUM"],
    "Entertainment": ["NETFLIX SUBSCRIPTION", "AMAZON PRIME", "PVR CINEMAS", "BOOKMYSHOW", "SPOTIFY", "STEAM GAMES", "CONCERT TICKET"],
    "Shopping": ["AMAZON.IN PURCHASE", "FLIPKART ORDER", "MYNTRA", "RELIANCE FRESH", "DMART", "ZUDIO", "H&M STORE", "IKEA"],
    "Salary": ["MONTHLY SALARY ACME", "PAYROLL DEPOSIT", "COMPANY WAGE"],
    "Freelance": ["UPWORK WITHDRAWAL", "FIVERR EARNINGS", "CLIENT PAYMENT", "CONSULTING FEE"],
    "Investment": ["MUTUAL FUND SIP", "STOCK DIVIDEND", "BOND INTEREST", "ZERODHA FUNDS"]
}

def generate_transactions(app):
    with app.app_context():
        # Fetch categories mapping
        categories = Category.query.all()
        cat_map = {cat.name: cat for cat in categories}
        
        # We need to make sure categories exist
        if not cat_map:
            print("Categories not found in DB! Run seed.py first.")
            return

        transactions_to_add = []
        base_date = datetime.now(timezone.utc) - timedelta(days=100)

        for category_name, merchants in MERCHANTS.items():
            if category_name not in cat_map:
                continue
            cat = cat_map[category_name]
            
            # Generate 20-30 transactions per category
            num_transactions = random.randint(20, 30)
            for _ in range(num_transactions):
                merchant = random.choice(merchants)
                
                # Add some random numbers to mimic real descriptions
                suffix = random.choice(["", f" #{random.randint(1000, 9999)}", f" TXN{random.randint(100, 999)}", " DEBIT"])
                description = f"{merchant}{suffix}"
                
                amount = random.uniform(100, 5000)
                if cat.type == "income":
                    amount = random.uniform(10000, 80000)
                
                date = base_date + timedelta(days=random.randint(0, 100))
                
                txn = Transaction(
                    amount=round(amount, 2),
                    description=description,
                    type=cat.type,
                    date=date.date(),
                    category_id=cat.id
                )
                transactions_to_add.append(txn)
        
        db.session.bulk_save_objects(transactions_to_add)
        db.session.commit()
        print(f"Seeded {len(transactions_to_add)} categorized transactions for ML training.")

if __name__ == "__main__":
    app = create_app()
    generate_transactions(app)
