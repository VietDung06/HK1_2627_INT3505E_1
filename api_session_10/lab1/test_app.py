import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest


sys.path.insert(0, str(Path(__file__).parent))

from app import app
from sunset import deprecate_at


@pytest.fixture()
def client():
    app.config.update(TESTING=True)
    with app.test_client() as test_client:
        yield test_client


def test_uri_path_versions(client):
    assert client.get("/api/v1/users/1").json["full_name"] == "Văn Nguyễn"
    assert client.get("/api/v2/users/1").json["first_name"] == "Văn"


def test_header_versioning(client):
    response = client.get("/api/header/users/1", headers={"X-API-Version": "1"})
    assert response.status_code == 200
    assert response.json["full_name"] == "Văn Nguyễn"
    assert response.headers["X-API-Version-Served"] == "1"
    assert client.get(
        "/api/header/users/1", headers={"X-API-Version": "99"}
    ).status_code == 400


def test_sunset_headers_and_gone():
    sunset = datetime.now(timezone.utc) + timedelta(days=1)

    @deprecate_at(sunset, replacement="/api/v2/users")
    def active():
        return {"ok": True}

    with app.test_request_context("/api/sunset/users/1"):
        response = active()
    assert response.json["ok"] is True

    @deprecate_at(datetime.now(timezone.utc) - timedelta(days=1))
    def expired():
        return {"ok": True}

    with app.test_request_context("/api/sunset/users/1"):
        assert expired()[1] == 410


def test_blue_green_routing(client):
    response = client.post("/api/orders", json={"account_id": "acct_42"})
    assert response.status_code == 201
    assert response.headers["X-Order-Handler"] == "v2"
    response = client.post(
        "/api/orders", json={"account_id": "ordinary"}, headers={"X-Cohort": "beta"}
    )
    assert response.headers["X-Order-Handler"] == "v2"


def test_query_parameter_versioning(client):
    response = client.get("/api/query/users/1?version=1")
    assert response.json["full_name"] == "Văn Nguyễn"
    assert response.headers["X-API-Version-Served"] == "1"
    assert client.get("/api/query/users/1?version=99").status_code == 400
