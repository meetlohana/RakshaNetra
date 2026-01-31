from flask import Blueprint, request, jsonify
import re
from utils.dashboard_updater import update_dashboard

url_bp = Blueprint("url_checker", __name__)

@url_bp.route(
    "/check-url",
    methods=["POST"],
    endpoint="check_url_api"
)
def check_url():
    data = request.get_json() or {}
    url = data.get("url", "").lower()

    score = 100
    reasons = []

    if not url.startswith("https://"):
        score -= 20
        reasons.append("URL does not use HTTPS")

    suspicious_words = ["login", "verify", "free", "account", "secure", "update"]
    for word in suspicious_words:
        if word in url:
            score -= 10
            reasons.append(f"Suspicious keyword found: {word}")

    score = max(score, 0)

    if score >= 75:
        risk = "LOW"
        status = "Secure"
    elif score >= 40:
        risk = "MEDIUM"
        status = "Suspicious"
    else:
        risk = "HIGH"
        status = "Dangerous"

    # ✅ ALWAYS update dashboard
    update_dashboard(risk, score)

    return jsonify({
        "url": url,
        "status": status,
        "risk": risk,
        "score": score,
        "reasons": reasons
    })
