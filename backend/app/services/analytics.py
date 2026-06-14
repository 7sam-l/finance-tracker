import pandas as pd
import numpy as np
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta

from app.models import Transaction, Category

def get_trends():
    """Returns monthly totals for the last 12 months, overall and by category."""
    end_date = datetime.now(timezone.utc).date()
    start_date = (end_date - relativedelta(months=11)).replace(day=1)
    
    transactions = Transaction.query.join(Category).filter(
        Transaction.date >= start_date,
        Transaction.type == 'expense'
    ).all()
    
    # Ensure all months are present
    all_months = [(start_date + relativedelta(months=i)).strftime('%Y-%m') for i in range(12)]
    
    if not transactions:
        return {"months": all_months, "overall": [0.0]*12, "by_category": {}}
        
    df = pd.DataFrame([{
        'date': t.date,
        'amount': float(t.amount),
        'category': t.category.name
    } for t in transactions])
    
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.strftime('%Y-%m')
    
    # Overall monthly trend
    overall = df.groupby('month')['amount'].sum().reset_index()
    
    # By category trend
    by_category = df.groupby(['month', 'category'])['amount'].sum().unstack(fill_value=0).reset_index()
    
    overall_dict = dict(zip(overall['month'], overall['amount']))
    overall_list = [overall_dict.get(m, 0.0) for m in all_months]
    
    cat_dict = {}
    for cat in df['category'].unique():
        if cat in by_category.columns:
            m_dict = dict(zip(by_category['month'], by_category[cat]))
            cat_dict[cat] = [m_dict.get(m, 0.0) for m in all_months]
            
    return {
        "months": all_months,
        "overall": overall_list,
        "by_category": cat_dict
    }

def get_anomalies():
    """Detect unusually large transactions using IQR per category."""
    # Look at last 6 months to define distribution, then check recent ones
    transactions = Transaction.query.join(Category).filter(
        Transaction.type == 'expense'
    ).all()
    
    if not transactions:
        return []
        
    df = pd.DataFrame([{
        'id': t.id,
        'date': t.date,
        'amount': float(t.amount),
        'description': t.description,
        'category': t.category.name,
        'category_id': t.category_id
    } for t in transactions])
    
    anomalies = []
    
    for cat in df['category'].unique():
        cat_df = df[df['category'] == cat]
        if len(cat_df) < 5:
            continue # Need minimum data points
            
        Q1 = cat_df['amount'].quantile(0.25)
        Q3 = cat_df['amount'].quantile(0.75)
        IQR = Q3 - Q1
        
        upper_bound = Q3 + 1.5 * IQR
        
        # Find anomalies in the last 30 days
        cutoff_date = datetime.now(timezone.utc).date() - relativedelta(days=30)
        recent_anomalies = cat_df[(cat_df['amount'] > upper_bound) & (pd.to_datetime(cat_df['date']).dt.date >= cutoff_date)]
        
        avg_spend = cat_df['amount'].mean()
        
        for _, row in recent_anomalies.iterrows():
            multiplier = row['amount'] / avg_spend if avg_spend > 0 else 0
            reason = f"{multiplier:.1f}x your average {cat} spend"
            anomalies.append({
                "transaction_id": row['id'],
                "date": row['date'].isoformat(),
                "description": row['description'],
                "category": row['category'],
                "amount": float(row['amount']),
                "reason": reason
            })
            
    # Sort by date descending
    anomalies.sort(key=lambda x: x['date'], reverse=True)
    return anomalies
