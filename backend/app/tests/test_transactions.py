from datetime import date


def get_category_id(client, name):
    cats = client.get("/api/categories/").get_json()
    return next((c["id"] for c in cats if c["name"] == name), None)


def create_transaction(client, **kwargs):
    payload = {"amount": 100.00, "description": "Test", "type": "income", "date": date.today().isoformat(), **kwargs}
    return client.post("/api/transactions/", json=payload)


class TestTransactionCreation:
    def test_create_income(self, client):
        res = create_transaction(client, category_id=get_category_id(client, "Salary"), type="income")
        assert res.status_code == 201

    def test_create_expense(self, client):
        res = create_transaction(client, category_id=get_category_id(client, "Food & Dining"), type="expense")
        assert res.status_code == 201

    def test_rejects_negative_amount(self, client):
        res = create_transaction(client, category_id=get_category_id(client, "Salary"), amount=-50)
        assert res.status_code == 400

    def test_rejects_zero_amount(self, client):
        res = create_transaction(client, category_id=get_category_id(client, "Salary"), amount=0)
        assert res.status_code == 400

    def test_rejects_future_date(self, client):
        res = create_transaction(client, category_id=get_category_id(client, "Salary"), date="2099-01-01")
        assert res.status_code == 400

    def test_rejects_type_mismatch(self, client):
        res = create_transaction(client, category_id=get_category_id(client, "Salary"), type="expense")
        assert res.status_code == 400

    def test_rejects_missing_category(self, client):
        res = create_transaction(client, category_id=9999)
        assert res.status_code == 400


class TestTransactionDelete:
    def test_delete_transaction(self, client):
        cat_id = get_category_id(client, "Salary")
        tx_id = create_transaction(client, category_id=cat_id).get_json()["id"]
        assert client.delete(f"/api/transactions/{tx_id}").status_code == 200

    def test_delete_nonexistent_returns_404(self, client):
        assert client.delete("/api/transactions/99999").status_code == 404


class TestSummary:
    def test_balance_is_correct(self, client):
        create_transaction(client, category_id=get_category_id(client, "Salary"), amount=1000, type="income")
        create_transaction(client, category_id=get_category_id(client, "Food & Dining"), amount=300, type="expense")
        data = client.get("/api/summary/").get_json()
        assert data["balance"] == 700.0

    def test_empty_summary_is_zero(self, client):
        data = client.get("/api/summary/").get_json()
        assert data["balance"] == 0.0
