from flask import Flask, jsonify, request

app = Flask(__name__)

# Dữ liệu giả lập
BOOKS = [
    {"id": "abc-1234", "t": "Python Basics"},
    {"id": "def-5678", "t": "Advanced Python"},
    {"id": "ghi-9012", "t": "Flask Web Development"},
]


def find_by_id(book_id):
    for book in BOOKS:
        if book["id"] == book_id:
            return book
    return None


# --- 1. PATH PARAMS (Biến bắt buộc trong URL) ---
@app.route("/books/<book_id>", methods=["GET"])
def get_book(book_id):
    book = find_by_id(book_id)
    if book is None:
        return jsonify({"error": "not found"}), 404
    return jsonify(book), 200


@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    return jsonify({"id": item_id}), 200


# --- 2. QUERY STRING (Bộ lọc tuỳ chọn) ---
@app.route("/books", methods=["GET"])
def list_books():
    limit = int(request.args.get("limit", 20))
    q = request.args.get("q", "").strip().lower()

    items = [b for b in BOOKS if q in b["t"].lower()]
    items = items[:limit]

    return jsonify({"items": items}), 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)