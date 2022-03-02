"""Test Database"""
import sqlite3

import pytest

from flaskApp.db import get_db


def test_get_close_db(app):
    """ Test closing database """
    with app.app_context():
        # pylint: disable=invalid-name
        db = get_db()
        assert db is get_db()

    # pylint: disable=invalid-name
    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute("SELECT 1")

    assert "closed" in str(e.value)


def test_init_db_command(runner, monkeypatch):
    """ Test initializing the database """
    # pylint: disable=too-few-public-methods
    class Recorder:
        """ Recorder class """
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr("flaskApp.db.init_db", fake_init_db)
    result = runner.invoke(args=["init-db"])
    assert "Initialized" in result.output
    assert Recorder.called
