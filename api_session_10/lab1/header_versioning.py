from functools import wraps

from flask import jsonify, request


SUPPORTED = {"1", "2", "2024-06-20"}
LATEST = "2"


def api_version(supported=SUPPORTED, default=LATEST):
    def decorate(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            version = request.headers.get("X-API-Version", default)
            if version not in supported:
                return jsonify(error="unsupported version"), 400
            result = function(version, *args, **kwargs)
            body, status = result if isinstance(result, tuple) else (result, 200)
            response = jsonify(body)
            response.status_code = status
            response.headers["X-API-Version-Served"] = version
            return response

        return wrapper

    return decorate
