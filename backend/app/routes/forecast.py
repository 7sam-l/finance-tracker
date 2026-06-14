from flask import Blueprint, jsonify
from ..services.forecaster import get_forecast_summary, get_forecast_by_category

bp = Blueprint("forecast", __name__)

@bp.route("/summary/", methods=["GET"])
def summary():
    return jsonify(get_forecast_summary()), 200

@bp.route("/by-category/", methods=["GET"])
def by_category():
    return jsonify(get_forecast_by_category()), 200
