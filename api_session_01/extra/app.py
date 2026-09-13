from flask import Flask, jsonify, request

app = Flask(__name__)

_next = 3
BOOKS = [
    {"id": 1, "title": "Clean Code", "author": "R. Martin", "year": 2008},
    {"id": 2, "title": "Refactoring", "author": "M. Fowler", "year": 1999},
]


def find(bid):
    return next((b for b in BOOKS if b["id"] == bid), None)


@app.route("/books", methods=["GET"])
def list_books():
    limit = int(request.args.get("limit", 100))
    q = request.args.get("q", "").strip().lower()
    sort_by = request.args.get("sort", "").strip().lower()

    results = BOOKS.copy()

    # (a) Tìm kiếm theo từ khóa q (tìm trong title hoặc author)
    if q:
        results = [
            b
            for b in results
            if q in b["title"].lower() or q in b["author"].lower()
        ]

    # (b) Sắp xếp danh sách (ví dụ: ?sort=title hoặc ?sort=year)
    if sort_by in ["title", "author", "year"]:
        results = sorted(results, key=lambda x: x.get(sort_by, ""))

    return jsonify(results[:limit]), 200


@app.route("/books/<int:bid>", methods=["GET"])
def get_book(bid):
    book = find(bid)
    if not book:
        return {"error": "not found"}, 404
    return jsonify(book), 200


@app.route("/books", methods=["POST"])
def create_book():
    global _next
    body = request.get_json(silent=True) or {}
    t, a, y = body.get("title"), body.get("author"), body.get("year")

    # Bắt buộc có title và author
    if not t or not a:
        return {"error": "need title+author"}, 400

    # (c) Bắt buộc field year là số int >= 1900
    if not isinstance(y, int) or y < 1900:
        return {"error": "year must be an integer >= 1900"}, 400

    book = {"id": _next, "title": t, "author": a, "year": y}
    _next += 1
    BOOKS.append(book)
    return jsonify(book), 201, {"Location": f"/books/{book['id']}"}


@app.route("/books/<int:bid>", methods=["PUT", "DELETE"])
def modify_book(bid):
    book = find(bid)
    if not book:
        return {"error": "not found"}, 404

    if request.method == "PUT":
        data = request.get_json(silent=True) or {}

        if "year" in data:
            y = data["year"]
            if not isinstance(y, int) or y < 1900:
                return {"error": "year must be an integer >= 1900"}, 400

        book.update(data)
        return jsonify(book), 200

    BOOKS.remove(book)
    return "", 204


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)