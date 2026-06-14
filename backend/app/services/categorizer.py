import os
import joblib

# Rule-based fallback dictionary
RULES = {
    "uber": "Transport",
    "ola": "Transport",
    "metro": "Transport",
    "petrol": "Transport",
    "swiggy": "Food & Dining",
    "zomato": "Food & Dining",
    "mcdonalds": "Food & Dining",
    "starbucks": "Food & Dining",
    "amazon": "Shopping",
    "flipkart": "Shopping",
    "myntra": "Shopping",
    "netflix": "Entertainment",
    "prime": "Entertainment",
    "spotify": "Entertainment",
    "jio": "Utilities",
    "airtel": "Utilities",
    "electricity": "Utilities",
    "hospital": "Healthcare",
    "apollo": "Healthcare",
    "pharmacy": "Healthcare"
}

_model = None

def get_model():
    global _model
    if _model is None:
        model_path = os.path.join(os.path.dirname(__file__), '..', '..', 'models', 'categorizer.pkl')
        if os.path.exists(model_path):
            try:
                _model = joblib.load(model_path)
            except Exception as e:
                print(f"Error loading model: {e}")
                _model = False # Mark as failed to load so we don't keep trying
        else:
            _model = False
    return _model if _model is not False else None

def predict_category(description: str) -> dict:
    """
    Predict the category of a transaction description.
    Returns a dict with:
    - predicted_category: str
    - confidence: float
    - method: str ('ml' or 'rule')
    """
    if not description:
        return {"predicted_category": "Other", "confidence": 0.0, "method": "rule"}
        
    model = get_model()
    
    if model:
        try:
            # The model is a pipeline with Tfidf and MultinomialNB
            probs = model.predict_proba([description])[0]
            max_prob_idx = probs.argmax()
            confidence = probs[max_prob_idx]
            predicted_category = model.classes_[max_prob_idx]
            
            # Use ML if confidence is reasonable
            if confidence > 0.5:
                return {
                    "predicted_category": predicted_category,
                    "confidence": float(confidence),
                    "method": "ml"
                }
        except Exception as e:
            print(f"ML prediction error: {e}")
            pass
            
    # Fallback to rule-based
    desc_lower = description.lower()
    for keyword, cat in RULES.items():
        if keyword in desc_lower:
            return {
                "predicted_category": cat,
                "confidence": 0.8, # hardcoded confidence for rules
                "method": "rule"
            }
            
    # Default fallback
    return {
        "predicted_category": "Other",
        "confidence": 0.0,
        "method": "rule"
    }
