import connexion
from flask_sqlalchemy import SQLAlchemy

# 1. Khởi tạo Connexion App
app = connexion.FlaskApp(__name__, specification_dir="openapi/")

# 2. Đăng ký spec YAML
app.add_api("products.yaml")

# 3. Lấy Flask app bên dưới để cấu hình Database
flask_app = app.app
flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///design_first.db"
flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# 4. Khởi tạo SQLAlchemy và liên kết với Flask app bằng init_app
db = SQLAlchemy()
db.init_app(flask_app)

# 5. Model Product
class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "price": self.price}

# 6. Tạo bảng tự động trong Database
with flask_app.app_context():
    db.create_all()

# 7. Handler functions
def list_products():
    # Sử dụng app_context hoặc truy vấn trực tiếp qua session
    rows = db.session.execute(db.select(Product)).scalars().all()
    return [p.to_dict() for p in rows], 200

def create_product(body):
    p = Product(name=body.get("name"), price=body.get("price"))
    db.session.add(p)
    db.session.commit()
    return p.to_dict(), 201

def get_product(id):
    p = db.get_or_404(Product, id)
    return p.to_dict(), 200

if __name__ == "__main__":
    app.run(port=8000)