from flask import Flask
from flask.views import MethodView
from flask_smorest import Api, Blueprint
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

# Khởi tạo Flask App & Cấu hình OpenAPI tự sinh
app = Flask(__name__)
app.config["API_TITLE"] = "Product API (Code-First)"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///code_first.db"

db = SQLAlchemy(app)
api = Api(app)

# 1. Model DB
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

# 2. Marshmallow Schemas (Dùng để Validate và Serialize)
class ProductSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)

class ProductInSchema(Schema):
    name = fields.Str(required=True)
    price = fields.Float(required=True)

# 3. Blueprint & Endpoints
blp = Blueprint("products", "products", url_prefix="/products")

@blp.route("")
class ProductList(MethodView):
    @blp.response(200, ProductSchema(many=True))
    def get(self):
        return db.session.execute(db.select(Product)).scalars().all()

    @blp.arguments(ProductInSchema)
    @blp.response(201, ProductSchema)
    def post(self, new_data):
        p = Product(**new_data)
        db.session.add(p)
        db.session.commit()
        return p

@blp.route("/<int:id>")
class ProductDetail(MethodView):
    @blp.response(200, ProductSchema)
    def get(self, id):
        return db.get_or_404(Product, id)

api.register_blueprint(blp)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(port=5000)