from flask import Blueprint, request, jsonify
import math
import re

from utils.dashboard_updater import update_dashboard

# ✅ Blueprint
password_bp = Blueprint("password", __name__)

@password_bp.route(
    "/check-password",
    methods=["POST"],
    endpoint="check_password_api"  # ✅ unique endpoint
)
def check_password():
    data = request.get_json() or {}
    password = data.get("password", "")

    reasons = []
    score = 0
    length = len(password)

    # 🔐 Length score
    if length >= 12:
        score += 30
    elif length >= 8:
        score += 20
        reasons.append("Password length should be at least 12 characters")
    else:
        reasons.append("Password too short")

    # 🔤 Character variety
    if re.search(r"[A-Z]", password):
        score += 15
    else:
        reasons.append("Missing uppercase letters")

    if re.search(r"[a-z]", password):
        score += 15
    else:
        reasons.append("Missing lowercase letters")

    if re.search(r"[0-9]", password):
        score += 15
    else:
        reasons.append("Missing numbers")

    if re.search(r"[^A-Za-z0-9]", password):
        score += 15
    else:
        reasons.append("Missing special characters")

    # 🔢 Entropy calculation
    charset = 0
    if re.search(r"[a-z]", password): charset += 26
    if re.search(r"[A-Z]", password): charset += 26
    if re.search(r"[0-9]", password): charset += 10
    if re.search(r"[^A-Za-z0-9]", password): charset += 32

    entropy = round(length * math.log2(charset)) if charset else 0

    # 🛡 Strength classification
    score = min(score, 100)

    if score >= 80:
        strength = "STRONG"
        status = "Secure"
    elif score >= 50:
        strength = "MEDIUM"
        status = "Average"
    else:
        strength = "WEAK"
        status = "Unsafe"
        update_dashboard(strength, score)


    return jsonify({
        "score": score,
        "strength": strength,
        "status": status,
        "entropy": entropy,
        "length": length,
        "reasons": reasons
    })
