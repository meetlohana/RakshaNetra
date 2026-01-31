from flask import Blueprint, request, jsonify
from datetime import datetime
import json
import os

from utils.dashboard_updater import update_dashboard

report_bp = Blueprint("report_scam", __name__)

REPORT_FILE = "reports.json"

@report_bp.route(
    "/report-scam",
    methods=["POST"],
    endpoint="report_scam_api"
)
def report_scam():
    data = request.get_json() or {}

    required_fields = ["category", "description", "platform", "date"]
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({
                "status": "ERROR",
                "message": f"Missing field: {field}"
            }), 400

    report = {
        "id": f"RN-{int(datetime.now().timestamp())}",
        "category": data["category"],
        "description": data["description"],
        "platform": data["platform"],
        "date": data["date"],
        "reported_at": datetime.now().isoformat()
    }

    reports = []
    if os.path.exists(REPORT_FILE):
        with open(REPORT_FILE, "r") as f:
            try:
                reports = json.load(f)
            except json.JSONDecodeError:
                reports = []

    reports.append(report)

    with open(REPORT_FILE, "w") as f:
        json.dump(reports, f, indent=2)

    return jsonify({
        "status": "SUCCESS",
        "message": "Scam reported successfully",
        "reference": report["id"]
    })
update_dashboard("HIGH", 40)
