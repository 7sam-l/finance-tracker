from app.services.analytics import get_trends, get_anomalies

def test_get_trends(client, app):
    with app.app_context():
        trends = get_trends()
        assert "months" in trends
        assert "overall" in trends
        assert "by_category" in trends
        assert len(trends["months"]) == 12

def test_get_anomalies(client, app):
    with app.app_context():
        anomalies = get_anomalies()
        assert isinstance(anomalies, list)
        # We might or might not have anomalies depending on the seed data
        if len(anomalies) > 0:
            assert "transaction_id" in anomalies[0]
            assert "reason" in anomalies[0]
