import sqlite3
from flask import Flask, jsonify, request, make_response

app = Flask(__name__)
DB_NAME = "database.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            isbn TEXT,
            price REAL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.get("/books")
def list_books():
    conn = get_db_connection()
    books_rows = conn.execute("SELECT * FROM books").fetchall()
    conn.close()

    books = [dict(row) for row in books_rows]
    return jsonify({"data": books, "total": len(books)}), 200

@app.post("/books")
def create_book():
    if not request.is_json:
        return jsonify(error="expected JSON"), 415

    p = request.get_json(silent=True) or {}
    t = (p.get("title") or "").strip()
    a = (p.get("author") or "").strip()

    if not t or not a:
        return jsonify(error="title and author required"), 422

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO books (title, author, isbn, price) VALUES (?, ?, ?, ?)",
        (t, a, p.get("isbn"), p.get("price"))
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    new_book = {"id": new_id, "title": t, "author": a, "isbn": p.get("isbn"), "price": p.get("price")}
    resp = make_response(jsonify(new_book), 201)
    resp.headers["Location"] = f"/books/{new_id}"
    return resp

@app.get("/books/<int:bid>")
def get_book(bid):
    conn = get_db_connection()
    book_row = conn.execute("SELECT * FROM books WHERE id = ?", (bid,)).fetchone()
    conn.close()

    if book_row is None:
        return jsonify(error="not found"), 404

    resp = make_response(jsonify(dict(book_row)), 200)
    resp.headers["Cache-Control"] = "public, max-age=60"
    return resp

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)