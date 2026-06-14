from flask import Blueprint, request, jsonify
from ..services.categorizer import predict_category
from ..utils import bad_request

bp = Blueprint("categorize", __name__)

@bp.route("/", methods=["POST"])
def categorize():
    json_data = request.get_json()
    if not json_data or "description" not in json_data:
        return bad_request("Missing 'description' in request body.")
        
    description = json_data["description"]
    prediction = predict_category(description)
    
    return jsonify(prediction), 200
