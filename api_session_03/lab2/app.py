import logging
from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException

logger = logging.getLogger(__name__)

class ProblemError(Exception):
    """Application error returned using the Problem Details format."""
    def __init__(self, title, detail, status):
        super().__init__(detail)
        self.title = title
        self.detail = detail
        self.status = status

def register_error_handler(app):

    @app.errorhandler(ProblemError)
    def handle_problem_error(error):
        response = jsonify({
            "type": request.path,
            "title": error.title,
            "status": error.status,
            "detail": error.detail,
            "instance": request.path, 
        })
        response.status_code = error.status
        response.content_type = "application/problem+json"
        return response

    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        response = jsonify({
            "type": request.path,
            "title": error.name,
            "status": error.code,
            "detail": error.description,
            "instance": request.path,  
        })
        response.status_code = error.code
        response.content_type = "application/problem+json"
        return response

    @app.errorhandler(Exception)
    def handle_unexpected_exception(error):
        logger.exception(
            "Unhandled exception while processing %s %s",
            request.method,
            request.path,
        )
        response = jsonify({
            "type": "about:blank",
            "title": "Internal Server Error",
            "status": 500,
            "detail": "An unexpected error occurred.",
            "instance": request.path,
        })
        response.status_code = 500
        response.content_type = "application/problem+json"
        return response

def create_app():
    app = Flask(__name__)
    register_error_handler(app)

    # Route demo để test lỗi 404
    @app.route("/resources/<int:resource_id>", methods=["GET"])
    def get_resource(resource_id):
        if resource_id == 999:  
            raise ProblemError(
                title="Resource Not Found",
                detail=f"Resource {resource_id} does not exist.",
                status=404
            )
        return jsonify({"id": resource_id, "name": "Sample Resource"})

    # Route demo để test lỗi Unhandled Exception (500)
    @app.route("/buggy-route", methods=["GET"])
    def buggy_route():
        return 1 / 0 

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)