from data.store import dashboard_data

def update_dashboard(risk, score):
    dashboard_data["total_scans"] += 1

    if risk in ["MEDIUM", "HIGH"]:
        dashboard_data["threats_found"] += 1

    if dashboard_data["threats_found"] > 10:
        dashboard_data["risk_level"] = "MEDIUM"
    if dashboard_data["threats_found"] > 20:
        dashboard_data["risk_level"] = "HIGH"

    dashboard_data["security_score"] = max(
        0,
        int((dashboard_data["security_score"] + score) / 2)
    )
