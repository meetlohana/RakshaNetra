from flask import Flask, jsonify
from flask_cors import CORS

from data.store import dashboard_data

from routes.url_checker import url_bp
from routes.password import password_bp
from routes.report_scam import report_bp
from routes.awareness import awareness_bp
from routes.vulnerability import vulnerability_bp
from routes.phishing import phishing_bp

app = Flask(__name__)
CORS(app)

# 🔐 Register Blueprints (API scoped)
app.register_blueprint(url_bp, url_prefix="/api")
app.register_blueprint(password_bp, url_prefix="/api")
app.register_blueprint(report_bp, url_prefix="/api")
app.register_blueprint(awareness_bp, url_prefix="/api")
app.register_blueprint(vulnerability_bp, url_prefix="/api")
app.register_blueprint(phishing_bp, url_prefix="/api")

@app.route("/")
def home():
    return jsonify({"message": "RakshaNetra Backend Running 🚀"})

@app.route("/api/dashboard-stats")
def dashboard_stats():
    return jsonify(dashboard_data)

if __name__ == "__main__":
    app.run(debug=True)
