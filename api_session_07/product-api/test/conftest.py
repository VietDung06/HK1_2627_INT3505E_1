import pytest
from ..wsgi import app

@pytest.fixture
def client(app):
    return app.test_client()