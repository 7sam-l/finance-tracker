import pytest
from app import create_app
from app.extensions import db as _db
from app.models import Category


@pytest.fixture
def app():
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})
    with app.app_context():
        _db.create_all()
        _db.session.add(Category(name="Salary", type="income"))
        _db.session.add(Category(name="Food & Dining", type="expense"))
        _db.session.commit()
        yield app
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()
