from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/check_age", methods=["POST"])
def check_age():
    data = request.get_json(silent=True) or {}
    if 'age' not in data:
        age = 0
    else:
        age = data.get('age')
    return jsonify({"your_age": age}), 200

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
