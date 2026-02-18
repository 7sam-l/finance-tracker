from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from ..extensions import db
from ..models import Category
from ..schemas import category_schema, categories_schema
from ..utils import not_found, bad_request
import logging

logger = logging.getLogger(__name__)
bp = Blueprint("categories", __name__)


@bp.route("/", methods=["GET"])
def list_categories():
    return jsonify(categories_schema.dump(Category.query.order_by(Category.name).all())), 200


@bp.route("/", methods=["POST"])
def create_category():
    json_data = request.get_json()
    if not json_data:
        return bad_request("No JSON body provided.")
    try:
        data = category_schema.load(json_data)
    except ValidationError as err:
        return bad_request(err.messages)
    if Category.query.filter_by(name=data["name"]).first():
        return bad_request({"name": ["Category with this name already exists."]})
    category = Category(name=data["name"], type=data["type"])
    db.session.add(category)
    db.session.commit()
    return jsonify(category_schema.dump(category)), 201
