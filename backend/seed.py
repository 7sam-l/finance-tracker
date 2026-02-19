from app import create_app
from app.extensions import db
from app.models import Category

DEFAULT_CATEGORIES = [
    {"name": "Salary", "type": "income"},
    {"name": "Freelance", "type": "income"},
    {"name": "Investment", "type": "income"},
    {"name": "Food & Dining", "type": "expense"},
    {"name": "Transport", "type": "expense"},
    {"name": "Utilities", "type": "expense"},
    {"name": "Healthcare", "type": "expense"},
    {"name": "Entertainment", "type": "expense"},
    {"name": "Shopping", "type": "expense"},
]

app = create_app()
with app.app_context():
    db.create_all()
    for cat_data in DEFAULT_CATEGORIES:
        if not Category.query.filter_by(name=cat_data["name"]).first():
            db.session.add(Category(**cat_data))
    db.session.commit()
    print("Seeded default categories.")
