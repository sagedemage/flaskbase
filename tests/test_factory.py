"""Test Factory"""
from flaskApp import create_app


def test_config():
    """Test create_app without passing test config."""
    assert not create_app().testing
    assert create_app({"TESTING": True}).testing


def test_hello(client):
    """Verify response value"""
    response = client.get("/hello")
    assert response.data == b"Hello, World!"
