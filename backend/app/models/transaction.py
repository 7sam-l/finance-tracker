from datetime import datetime, timezone
from ..extensions import db


class Category(db.Model): #Model Schema for Category
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    type = db.Column(db.String(10), nullable=False)
    transactions = db.relationship("Transaction", back_populates="category", lazy=True)

    def to_dict(self): 
        return {"id": self.id, "name": self.name, "type": self.type}


class Transaction(db.Model): #for Transaction
    __tablename__ = "transactions"
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(10), nullable=False)
    date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    category = db.relationship("Category", back_populates="transactions")

    def to_dict(self): 
        return {
            "id": self.id,
            "amount": float(self.amount),
            "description": self.description,
            "type": self.type,
            "date": self.date.isoformat(),
            "created_at": self.created_at.isoformat(),
            "category": self.category.to_dict(),
        }
