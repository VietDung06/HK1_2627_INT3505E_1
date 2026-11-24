from datetime import datetime, timezone
from email.utils import format_datetime
from functools import wraps
import logging

from flask import jsonify, request


log = logging.getLogger("sunset")
DEFAULT_SUNSET = datetime(2026, 12, 31, 23, 59, 59, tzinfo=timezone.utc)


def http_date(value):
    return format_datetime(value, usegmt=True)


def deprecate_at(sunset_date=DEFAULT_SUNSET, replacement=None):
    def decorate(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            if datetime.now(timezone.utc) >= sunset_date:
                return jsonify({
                    "error": "gone",
                    "sunset": http_date(sunset_date),
                    "use_instead": replacement,
                }), 410
            result = function(*args, **kwargs)
            body, status = result if isinstance(result, tuple) else (result, 200)
            response = jsonify(body)
            response.status_code = status
            response.headers["Sunset"] = http_date(sunset_date)
            response.headers["Deprecation"] = "true"
            if replacement:
                response.headers["Link"] = (
                    f"<{replacement}>; rel=\"successor-version\""
                )
            log.warning("deprecated_call %s %s", request.path, request.remote_addr)
            return response

        return wrapper

    return decorate
