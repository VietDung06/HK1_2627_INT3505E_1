from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from ..extensions import db
from ..models import Product
from ..api.errors import Conflict
from ..api.schemas import (
    ProductOut, ProductIn, ProductPatch, ReserveIn)

orders_bp = Blueprint(
    "orders", __name__, url_prefix="/api/v1/orders")