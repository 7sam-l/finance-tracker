from app.services.forecaster import get_forecast_summary, get_forecast_by_category

def test_forecast_summary(client, app):
    # App context is needed for DB queries
    with app.app_context():
        summary = get_forecast_summary()
        assert "month" in summary
        assert "predicted_total_expense" in summary
        assert "predicted_total_income" in summary
        assert "predicted_net" in summary
        assert "confidence_interval" in summary
        assert "method" in summary

def test_forecast_by_category(client, app):
    with app.app_context():
        cat_forecast = get_forecast_by_category()
        assert "month" in cat_forecast
        assert "forecast" in cat_forecast
        assert isinstance(cat_forecast["forecast"], list)
