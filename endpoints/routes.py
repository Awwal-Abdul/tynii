from flask import Blueprint, jsonify


api_bp = Blueprint("api", __name__)


@api_bp.get("/api/data")
def register_link():
    return jsonify({"message": "Successful"})
