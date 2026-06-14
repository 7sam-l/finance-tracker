from app.services.categorizer import predict_category

def test_categorizer_rule_based_fallback():
    # Test known rules
    pred = predict_category("UBER RIDE")
    assert pred["predicted_category"] == "Transport"
    assert pred["method"] == "rule"
    
    pred = predict_category("SWIGGY DINNER")
    assert pred["predicted_category"] == "Food & Dining"
    assert pred["method"] == "rule"

def test_categorizer_empty_description():
    pred = predict_category("")
    assert pred["predicted_category"] == "Other"
    
def test_categorizer_unknown():
    pred = predict_category("SOMETHING UNKNOWN ENTIRELY 123")
    # Will probably fallback to rule based "Other" if ML model isn't very confident
    # or if ML is active it might predict something. Just ensure it returns the right shape.
    assert "predicted_category" in pred
    assert "confidence" in pred
    assert "method" in pred
