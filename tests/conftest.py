"""Configuration Test"""
import os
import tempfile

import pytest
from flaskApp import create_app
from flaskApp.db import get_db
from flaskApp.db import init_db

# read in SQL for populating test data
with open(os.path.join(os.path.dirname(__file__), "data.sql"), "rb") as f:
    _data_sql = f.read().decode("utf8")


# pylint: disable=redefined-outer-name
@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()
    # create the app with common test config
    app = create_app({"TESTING": True, "DATABASE": db_path})

    # create the database and load test data
    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    # close and remove the temporary database
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


class AuthActions:
    """Authentication Actions"""
    def __init__(self, client):
        self._client = client

    def login(self, username="test", password="test"):
        """Login the user"""
        return self._client.post(
            "/auth/login", data={"username": username, "password": password}
        )

    def logout(self):
        """Logout the user"""
        return self._client.get("/auth/logout")


@pytest.fixture
def auth(client):
    """Authenticate the user"""
    return AuthActions(client)
