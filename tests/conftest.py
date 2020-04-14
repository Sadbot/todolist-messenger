import pytest
from aiohttp.test_utils import TestClient

from todolist.app import init_app
from todolist.settings import get_config


@pytest.fixture
async def client(aiohttp_client) -> TestClient:
    config = get_config()
    app = await init_app(config)
    return await aiohttp_client(app)
