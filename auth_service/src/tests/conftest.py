import asyncio
from dataclasses import dataclass
from http.client import HTTPResponse
from typing import AsyncGenerator

import aiohttp
import psycopg2
import pytest
import pytest_asyncio
from aioredis import Redis, create_redis
from multidict import CIMultiDictProxy

from .config import TestConfig


@pytest.fixture(scope='session')
def config() -> TestConfig:
    return TestConfig()


@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session')
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest_asyncio.fixture(scope='session')
async def redis(config) -> AsyncGenerator[Redis, None]:
    redis = await create_redis((config.redis_host, config.redis_port))
    await redis.flushall()
    yield redis
    redis.close()
    await redis.wait_closed()


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest_asyncio.fixture
def make_request(session, config):
    method_type = {
        'patch': session.patch,
        'delete': session.delete,
        'get': session.get,
        'post': session.post
    }

    async def inner(method: str, json: dict = None, headers: dict = None,
                    method_type_choice: str = 'post') -> HTTPResponse:
        url = f'{config.service_url}{method}'
        async with method_type[method_type_choice](url, json=json, headers=headers) as response:
            return HTTPResponse(
              body=await response.json(),
              headers=response.headers,
              status=response.status,
            )
    return inner


@pytest_asyncio.fixture(scope='function')
def restart_db(config):
    conn = psycopg2.connect(
        host=config.postrges_host,
        database=config.postrges_db,
        user=config.postrges_user,
        password=config.postrges_pass)
    cur = conn.cursor()
    cur.execute('delete from provider_users')
    cur.execute('delete from users_role')
    cur.execute('delete from history')
    cur.execute('delete from users')
    cur.execute('delete from role')
    cur.execute("INSERT INTO role(id, created, modified, name) VALUES("
                "'8f5800cc-aa9c-4db8-b7f1-cbba98b9de2c','2022-06-05 09:08:04.474792',"
                "'2022-06-05 09:08:04.474792', 'premium')")
    cur.execute("INSERT INTO role(id, created, modified, name) VALUES("
                "'7b024dc7-891c-4cbe-8b4e-6c5c11b2186b','2022-06-05 09:08:04.474792',"
                "'2022-06-05 09:08:04.474792', 'superuser')")

    cur.execute("INSERT INTO users(id, created, username, modified, password, email, email_verified) VALUES("
                "'5a7e9761-994f-4395-8982-ade82fd1a6ed', '2022-06-06 05:00:15.668604', 'superuser',"   
                "'2022-06-06 05:00:15.668604', '83234657c5df8232839ac8c0572e158d', 'admin@test.com', True)")

    cur.execute("INSERT INTO users_role(id, created, user_id, role_id) VALUES("
                "'5a7e9761-994f-4395-8982-add82fd1a6ed','2022-06-05 09:08:04.474792',"
                "'5a7e9761-994f-4395-8982-ade82fd1a6ed', '7b024dc7-891c-4cbe-8b4e-6c5c11b2186b')")
    conn.commit()
    conn.close()
