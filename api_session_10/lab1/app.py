from flask import Flask, jsonify, request

from blueprints.users_data import get_user
from blueprints.v1 import bp as v1_bp
from blueprints.v2 import bp as v2_bp
from gateway import dispatch
from header_versioning import api_version
from sunset import deprecate_at


app = Flask(__name__)
app.register_blueprint(v1_bp, url_prefix="/api/v1/users")
app.register_blueprint(v2_bp, url_prefix="/api/v2/users")


@app.route("/api/header/users/<int:uid>")
@api_version()
def header_user(version, uid):
    user = get_user(uid)
    if not user:
        return {"error": "nf"}, 404
    if version == "1":
        return {"id": uid, "full_name": f"{user['first_name']} {user['last_name']}"}
    return {
        "id": uid,
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "email": user["email"],
    }


@app.route("/api/query/users/<int:uid>")
def query_user(uid):
    version = request.args.get("version", "2")
    if version not in {"1", "2"}:
        return jsonify(error="unsupported version"), 400
    user = get_user(uid)
    if not user:
        return jsonify(error="nf"), 404
    body = (
        {"id": uid, "full_name": f"{user['first_name']} {user['last_name']}"}
        if version == "1"
        else {
            "id": uid,
            "first_name": user["first_name"],
            "last_name": user["last_name"],
            "email": user["email"],
        }
    )
    response = jsonify(body)
    response.headers["X-API-Version-Served"] = version
    return response


@app.route("/api/sunset/users/<int:uid>")
@deprecate_at(replacement="/api/v2/users")
def sunset_user(uid):
    user = get_user(uid)
    if not user:
        return {"error": "nf"}, 404
    return {"id": uid, "full_name": f"{user['first_name']} {user['last_name']}"}


@app.post("/api/orders")
def create_order():
    body = request.get_json(silent=True)
    if not isinstance(body, dict):
        return jsonify(error="JSON object required"), 400
    version, result = dispatch(body)
    response = jsonify(result)
    response.headers["X-Order-Handler"] = version
    return response, 201 if version == "v2" else 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
