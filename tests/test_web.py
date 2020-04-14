import pytest
from aiohttp.test_utils import TestClient


# @pytest.mark.skip(reason='fix db connection')
async def test_msg_sending(client: TestClient):
    resp = await client.get('/')
    assert resp.status == 200
