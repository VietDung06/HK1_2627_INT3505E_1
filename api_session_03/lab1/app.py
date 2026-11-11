# 4. Triển khai Flask Routes cho Collection

from flask import Flask, request, jsonify

app = Flask(__name__)

POSTS_DB = []

@app.route('/api/v1/posts', methods=['GET'])
def get_posts():
    tag = request.args.get('tag')
    author_id = request.args.get('author_id')
    page = int(request.args.get('page', 1))
    per_page = min(int(request.args.get('per_page', 10)), 100) 

    results = POSTS_DB

    if tag:
        results = [p for p in results if tag in p.get('tags', [])]
    if author_id:
        results = [p for p in results if str(p.get('author_id')) == author_id]

    start = (page - 1) * per_page
    end = start + per_page
    paginated_results = results[start:end]

    return jsonify({
        "data": paginated_results,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": len(results)
        }
    }), 200


@app.route('/api/v1/posts', methods=['POST'])
def create_post():

    data = request.get_json()
    
    if not data or 'title' not in data or 'content' not in data:
        return jsonify({
            "type": "https://api.blog.example/probs/invalid-body",
            "title": "Bad Request",
            "status": 400,
            "detail": "Thiếu trường 'title' hoặc 'content' bắt buộc."
        }), 400

    new_post = {
        "id": len(POSTS_DB) + 1,
        "title": data['title'],
        "content": data['content'],
        "author_id": data.get('author_id', 1),
        "tags": data.get('tags', [])
    }
    
    POSTS_DB.append(new_post)

    response = jsonify(new_post)
    response.status_code = 201
    response.headers['Location'] = f"/api/v1/posts/{new_post['id']}"
    return response

if __name__ == '__main__':
    app.run(debug=True)