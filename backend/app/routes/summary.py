from flask import Blueprint, jsonify
from sqlalchemy import func
from ..extensions import db
from ..models import Transaction, Category

bp = Blueprint("summary", __name__)


@bp.route("/", methods=["GET"])
def get_summary():
    def total_by_type(tx_type):
        result = db.session.query(func.sum(Transaction.amount)).filter_by(type=tx_type).scalar()
        return float(result) if result else 0.0

    total_income = total_by_type("income")
    total_expenses = total_by_type("expense")

    breakdown_rows = (
        db.session.query(Transaction.category_id, Transaction.type, func.sum(Transaction.amount).label("total"))
        .group_by(Transaction.category_id, Transaction.type)
        .all()
    )

    breakdown = []
    for category_id, tx_type, total in breakdown_rows:
        cat = Category.query.get(category_id)
        breakdown.append({"category": cat.name if cat else "Unknown", "type": tx_type, "total": float(total)})

    return jsonify({
        "total_income": total_income,
        "total_expenses": total_expenses,
        "balance": total_income - total_expenses,
        "breakdown": breakdown,
    }), 200
