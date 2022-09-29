import asyncio
from dataclasses import dataclass
from http.client import HTTPResponse

import aiohttp
import pytest_asyncio
from multidict import CIMultiDictProxy

from .config import TestConfig


@pytest_asyncio.fixture(scope="session")
def config() -> TestConfig:
    return TestConfig()


@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest_asyncio.fixture
def make_get_request(session, config):
    async def inner(method: str, params: dict = None, headers: dict = None) -> HTTPResponse:
        params = params or {}
        headers = headers or {}
        url = f"{config.service_url}{method}"
        async with session.get(url, params=params, headers=headers) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner
