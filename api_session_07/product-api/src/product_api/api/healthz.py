from flask import Blueprint, jsonify
from sqlalchemy import text
from ..extensions import db
health_bp = Blueprint("health", __name__, url_prefix="")
# liveness — không DB
@health_bp.get("/healthz")
def liveness():
    return jsonify({"status": "ok"}), 200