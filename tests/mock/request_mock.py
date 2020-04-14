import asyncio

from aiohttp import ClientResponse
from aiohttp.helpers import TimerNoop
from unittest import mock
from yarl import URL


class RequestMock:
    def __init__(self, requests: list):
        self.requests = requests

    async def request(self, *args, **kwargs) -> ClientResponse:
        try:
            data = self.requests.pop(0)
            response = ClientResponse('get', URL('http://def-cl-resp.org'),
                                      request_info=mock.Mock(),
                                      writer=mock.Mock(),
                                      continue100=None,
                                      timer=TimerNoop(),
                                      traces=[],
                                      loop=asyncio.get_running_loop(),
                                      session=mock.Mock())
            response.status = 200
            response._body = data
            response._headers = {'Content-Type': 'application/json'}
            return response

        except IndexError as e:
            print(f'error in pop requests')
            raise Exception(str(e)) from e
