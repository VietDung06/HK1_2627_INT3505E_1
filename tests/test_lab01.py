"""LAB 1 — add your five tests here. Do not delete the smoke tests.

A. GET /books, empty database -> HTTP 200 and []
B. GET /books/9999 -> HTTP 404, JSON code == NOT_FOUND
C. POST /books with only author -> HTTP 400, errors contains title
D. POST valid book, DELETE it, GET same id -> HTTP 404
BONUS. Validate a Book response using JSON Schema; add an unknown
       field to a *copy* of the response and assert ValidationError.

Useful imports:
    from jsonschema import validate, ValidationError
    import pytest
    from tools import get_book_schema

Do not depend on test execution order. Fixtures: client, app, sample_book.
"""
import pytest

# A. GET /books khi CSDL rỗng trả về mảng rỗng [] (không phải null)
def test_get_books_empty(client):
    response = client.get("/books")
    assert response.status_code == 200
    assert response.content_type == "application/json"
    data = response.get_json()
    assert data == []
    assert data is not None

# B. GET /books/<id> với id không tồn tại trả về 404 + JSON chứa "code": "NOT_FOUND"
def test_get_book_not_found(client):
    response = client.get("/books/9999")
    assert response.status_code == 404
    data = response.get_json()
    assert data.get("code") == "NOT_FOUND"

# C. POST /books thiếu title trả về 400 + trong errors có field "title"
def test_post_book_missing_title(client):
    payload = {"author": "Unknown Author", "year": 2024}
    response = client.post("/books", json=payload)
    assert response.status_code == 400
    
    data = response.get_json()
    errors = data.get("errors", [])
    fields = {e["field"] for e in errors}
    assert "title" in fields

# D. Xoá rồi GET cùng id — phải trả về 404
def test_delete_then_get_returns_404(client, sample_book):
    # sample_book fixture trả về id của cuốn sách đã được tạo sẵn trong CSDL
    book_id = sample_book

    # Thực hiện xoá sách
    delete_res = client.delete(f"/books/{book_id}")
    assert delete_res.status_code in [200, 204]

    # Kiểm tra lại bằng GET -> phải trả về 404
    get_res = client.get(f"/books/{book_id}")
    assert get_res.status_code == 404


# BONUS. Viết Test Case Bonus (`test_response_extra_field_blocked`)

from jsonschema import validate, ValidationError

# Cấu hình Schema không cho phép các trường thừa ngoài định nghĩa
BOOK_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "title": {"type": "string"},
        "author": {"type": "string"},
        "year": {"type": "integer"},
        "isbn": {"type": ["string", "null"]}
    },
    "required": ["id", "title", "author"],
    "additionalProperties": False  # Chặn tất cả các trường lạ/bất thường
}

def test_response_extra_field_blocked(client, app):
    from models import db, Book

    # Giả lập thêm một field lạ/nhạy cảm (ví dụ: password_hash) vào CSDL
    with app.app_context():
        book = Book(title="Clean Code", author="Robert C. Martin", year=2008)
        # Giả lập gắn trường lạ nếu object có hỗ trợ hoặc dictionary response có chứa trường thừa
        db.session.add(book)
        db.session.commit()
        book_id = book.id

    # Lấy dữ liệu từ API
    response = client.get(f"/books/{book_id}")
    data = response.get_json()

    # Kiểm tra dữ liệu response có khớp với schema hay không
    # Nếu backend lộ trường lạ như password_hash, validate() sẽ bắt lỗi
    validate(instance=data, schema=BOOK_SCHEMA)

    # Thử cố tình add thêm trường lạ để chứng minh jsonschema sẽ chối bỏ (bắt được lỗi)
    bad_data = data.copy()
    bad_data["password_hash"] = "secret_hash_123"
    
    with pytest.raises(ValidationError):
        validate(instance=bad_data, schema=BOOK_SCHEMA)