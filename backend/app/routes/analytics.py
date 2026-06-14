from flask import Blueprint, jsonify
from ..services.analytics import get_trends, get_anomalies

bp = Blueprint("analytics", __name__)

@bp.route("/trends/", methods=["GET"])
def trends():
    return jsonify(get_trends()), 200

@bp.route("/anomalies/", methods=["GET"])
def anomalies():
    return jsonify(get_anomalies()), 200
