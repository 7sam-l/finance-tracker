import pandas as pd
import numpy as np
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
from statsmodels.tsa.holtwinters import ExponentialSmoothing

from app.models import Transaction, Category

def get_monthly_series(category_name=None):
    query = Transaction.query.join(Category).filter(Transaction.type == 'expense')
    if category_name:
        query = query.filter(Category.name == category_name)
        
    transactions = query.all()
    if not transactions:
        return pd.Series(dtype=float)
        
    # Convert to DataFrame
    df = pd.DataFrame([{
        'date': t.date,
        'amount': float(t.amount)
    } for t in transactions])
    
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    
    # Resample to monthly totals
    monthly = df.resample('ME').sum()['amount']
    # Fill missing months with 0
    if len(monthly) > 0:
        idx = pd.date_range(start=monthly.index.min(), end=monthly.index.max(), freq='ME')
        monthly = monthly.reindex(idx, fill_value=0)
    
    return monthly

def forecast_series(series: pd.Series, steps=1) -> dict:
    if len(series) == 0:
        return {"prediction": 0.0, "ci_lower": 0.0, "ci_upper": 0.0, "method": "none"}
        
    if len(series) < 6:
        # Not enough data for Holt-Winters, use moving average of last 3 months
        # Or whatever is available
        window = min(len(series), 3)
        pred = series.iloc[-window:].mean()
        std = series.iloc[-window:].std() if window > 1 else pred * 0.1
        if pd.isna(std): std = pred * 0.1
        
        return {
            "prediction": float(pred),
            "ci_lower": max(0.0, float(pred - std)),
            "ci_upper": float(pred + std),
            "method": "moving_average"
        }
        
    # Holt-Winters
    # Since data might have 0s, add a tiny epsilon if needed, or don't use multiplicative
    try:
        model = ExponentialSmoothing(series, trend='add', seasonal=None, initialization_method="estimated")
        fit_model = model.fit()
        forecast = fit_model.forecast(steps)
        
        # Simple confidence interval based on residuals
        residuals = fit_model.resid
        std_resid = residuals.std()
        
        pred = forecast.iloc[0]
        return {
            "prediction": float(pred),
            "ci_lower": max(0.0, float(pred - std_resid)),
            "ci_upper": float(pred + std_resid),
            "method": "holt_winters"
        }
    except Exception as e:
        print(f"Forecasting error: {e}")
        # Fallback to moving average on error
        window = 3
        pred = series.iloc[-window:].mean()
        std = series.iloc[-window:].std()
        if pd.isna(std): std = pred * 0.1
        return {
            "prediction": float(pred),
            "ci_lower": max(0.0, float(pred - std)),
            "ci_upper": float(pred + std),
            "method": "moving_average_fallback"
        }

def get_forecast_summary():
    # Overall expenses
    expense_series = get_monthly_series()
    expense_forecast = forecast_series(expense_series)
    
    # Overall income (just use simple avg)
    income_query = Transaction.query.join(Category).filter(Transaction.type == 'income').all()
    predicted_income = 0.0
    if income_query:
        df_inc = pd.DataFrame([{'date': t.date, 'amount': float(t.amount)} for t in income_query])
        df_inc['date'] = pd.to_datetime(df_inc['date'])
        df_inc.set_index('date', inplace=True)
        inc_monthly = df_inc.resample('ME').sum()['amount']
        if len(inc_monthly) > 0:
            predicted_income = float(inc_monthly.iloc[-min(3, len(inc_monthly)):].mean())
            
    predicted_net = predicted_income - expense_forecast["prediction"]
    
    next_month = (datetime.now(timezone.utc) + relativedelta(months=1)).strftime('%Y-%m')
    
    return {
        "month": next_month,
        "predicted_total_expense": expense_forecast["prediction"],
        "predicted_total_income": predicted_income,
        "predicted_net": predicted_net,
        "confidence_interval": [expense_forecast["ci_lower"], expense_forecast["ci_upper"]],
        "method": expense_forecast["method"]
    }

def get_forecast_by_category():
    categories = Category.query.filter_by(type='expense').all()
    forecasts = []
    
    next_month = (datetime.now(timezone.utc) + relativedelta(months=1)).strftime('%Y-%m')
    
    for cat in categories:
        series = get_monthly_series(cat.name)
        if len(series) > 0:
            f = forecast_series(series)
            forecasts.append({
                "category": cat.name,
                "predicted_amount": f["prediction"]
            })
            
    return {
        "month": next_month,
        "forecast": forecasts
    }
