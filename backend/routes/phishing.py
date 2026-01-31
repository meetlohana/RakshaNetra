from flask import Blueprint, request, jsonify
import re
from utils.dashboard_updater import update_dashboard


phishing_bp = Blueprint("phishing", __name__)

PHISHING_KEYWORDS = [
    "urgent", "verify", "suspended", "account locked", "click here",
    "otp", "password", "login", "bank", "upi", "reset",
    "confirm", "limited time", "act now", "payment", "security alert"
]

SUSPICIOUS_DOMAINS = [
    ".xyz", ".site", ".top", ".click", ".online", ".tk", "bit.ly", "tinyurl"
]

@phishing_bp.route(
    "/check-phishing",
    methods=["POST"],
    endpoint="check_phishing_api"
)
def check_phishing():
    data = request.get_json() or {}
    text = data.get("text", "").lower()

    score = 100
    reasons = []

    # Keyword detection
    for word in PHISHING_KEYWORDS:
        if word in text:
            score -= 10
            reasons.append(f"Suspicious keyword detected: {word}")

    # URL detection
    urls = re.findall(r"https?://[^\s]+", text)
    if urls:
        score -= 15
        reasons.append("Message contains URL")

        for url in urls:
            for domain in SUSPICIOUS_DOMAINS:
                if domain in url:
                    score -= 20
                    reasons.append(f"Suspicious domain detected: {domain}")

    score = max(score, 0)

    if score >= 75:
        risk = "LOW"
        status = "Safe"
    elif score >= 40:
        risk = "MEDIUM"
        status = "Suspicious"
    else:
        risk = "HIGH"
        status = "Phishing Detected"
        update_dashboard(risk, score)


    return jsonify({
        "risk": risk,
        "status": status,
        "score": score,
        "reasons": reasons
    })
