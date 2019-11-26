import os
from pathlib import Path

import pytest
from sanic.websocket import WebSocketProtocol

from src import create_app
from src.utils.general import load_settings_from_environments



@pytest.fixture(scope='session')
def settings():

    dotenv_filepath = Path('.') / '.env'
    _settings = load_settings_from_environments(dotenv_path=dotenv_filepath, verbose=False)

    yield _settings

@pytest.fixture(scope='session')
def app(settings):
    app = create_app(settings)
    yield app


@pytest.fixture
def test_cli(loop, app, sanic_client):
    client = sanic_client(app, protocol=WebSocketProtocol)
    return loop.run_until_complete(client)
