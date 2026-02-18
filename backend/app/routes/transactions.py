from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from ..extensions import db
from ..models import Transaction, Category
from ..schemas import transaction_schema, transactions_schema
from ..utils import not_found, bad_request
import logging

logger = logging.getLogger(__name__)
bp = Blueprint("transactions", __name__)


@bp.route("/", methods=["GET"])
def list_transactions():
    tx_type = request.args.get("type")
    category_id = request.args.get("category_id", type=int)
    query = Transaction.query.order_by(Transaction.date.desc())
    if tx_type in ("income", "expense"):
        query = query.filter_by(type=tx_type)
    if category_id:
        query = query.filter_by(category_id=category_id)
    return jsonify(transactions_schema.dump(query.all())), 200


@bp.route("/", methods=["POST"])
def create_transaction():
    json_data = request.get_json()
    if not json_data:
        return bad_request("No JSON body provided.")
    try:
        data = transaction_schema.load(json_data)
    except ValidationError as err:
        return bad_request(err.messages)

    category = Category.query.get(data["category_id"])
    if not category:
        return bad_request({"category_id": ["Category does not exist."]})
    if data["type"] != category.type:
        return bad_request({"type": [f"Transaction type must match category type '{category.type}'."]})

    transaction = Transaction(
        amount=data["amount"],
        description=data["description"],
        type=data["type"],
        date=data["date"],
        category_id=data["category_id"],
    )
    db.session.add(transaction)
    db.session.commit()
    logger.info(f"Created transaction id={transaction.id}")
    return jsonify(transaction_schema.dump(transaction)), 201


@bp.route("/<int:transaction_id>", methods=["DELETE"])
def delete_transaction(transaction_id):
    transaction = Transaction.query.get(transaction_id)
    if not transaction:
        return not_found("Transaction")
    db.session.delete(transaction)
    db.session.commit()
    return jsonify({"message": "Transaction deleted."}), 200
