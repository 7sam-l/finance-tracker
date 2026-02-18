from flask import jsonify
import logging

logger = logging.getLogger(__name__)


def error_response(message, status_code, details=None):
    payload = {"error": message}
    if details:
        payload["details"] = details
    logger.warning(f"[{status_code}] {message} | details={details}")
    return jsonify(payload), status_code


def not_found(resource="Resource"):
    return error_response(f"{resource} not found.", 404)


def bad_request(details=None):
    return error_response("Invalid request data.", 400, details)
