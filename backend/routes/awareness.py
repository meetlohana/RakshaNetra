from flask import Blueprint, jsonify
import json

awareness_bp = Blueprint("awareness", __name__)

@awareness_bp.route("/api/awareness", methods=["GET"])
def get_awareness():
    with open("data/awareness.json", "r") as f:
        data = json.load(f)
    return jsonify(data)
