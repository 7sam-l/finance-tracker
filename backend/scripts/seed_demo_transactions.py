import os
import sys
from datetime import datetime, timezone, timedelta
from dateutil.relativedelta import relativedelta
import random

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.extensions import db
from app.models import Category, Transaction

def generate_history(app):
    with app.app_context():
        categories = Category.query.all()
        cat_map = {cat.name: cat for cat in categories}
        if not cat_map:
            print("Categories not found in DB! Run seed.py first.")
            return

        transactions_to_add = []
        now = datetime.now(timezone.utc)
        start_date = now - relativedelta(months=18)
        
        print(f"Generating 18 months of data starting from {start_date.strftime('%Y-%m-%d')}...")

        # Monthly base expenses to simulate typical user behavior
        monthly_base = {
            "Food & Dining": 5000,
            "Transport": 3000,
            "Utilities": 2500,
            "Healthcare": 1000,
            "Entertainment": 2000,
            "Shopping": 4000,
        }

        # Iterate month by month
        curr_date = start_date
        while curr_date <= now:
            # Salary
            txn = Transaction(
                amount=75000 + random.randint(-2000, 5000),
                description="MONTHLY SALARY ACME",
                type="income",
                date=curr_date.replace(day=1).date(),
                category_id=cat_map["Salary"].id
            )
            transactions_to_add.append(txn)

            # Generate expenses
            for cat_name, base_amount in monthly_base.items():
                if cat_name not in cat_map:
                    continue
                cat = cat_map[cat_name]
                
                # Seasonality: Higher shopping and entertainment in Nov/Dec
                multiplier = 1.0
                if curr_date.month in [11, 12] and cat_name in ["Shopping", "Entertainment"]:
                    multiplier = 1.8
                
                target_spend = base_amount * multiplier * random.uniform(0.8, 1.2)
                current_spend = 0
                
                # Create transactions until we reach target spend
                while current_spend < target_spend:
                    txn_amount = random.uniform(200, 1500)
                    if current_spend + txn_amount > target_spend:
                        txn_amount = target_spend - current_spend
                    
                    if txn_amount < 10:
                        break
                        
                    txn_date = curr_date.replace(day=random.randint(1, 28))
                    
                    transactions_to_add.append(Transaction(
                        amount=round(txn_amount, 2),
                        description=f"Synthetic {cat_name} Txn",
                        type="expense",
                        date=txn_date.date(),
                        category_id=cat.id
                    ))
                    current_spend += txn_amount

            curr_date += relativedelta(months=1)

        db.session.bulk_save_objects(transactions_to_add)
        db.session.commit()
        print(f"Seeded {len(transactions_to_add)} historical transactions.")

if __name__ == "__main__":
    app = create_app()
    generate_history(app)
