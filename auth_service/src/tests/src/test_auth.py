from http import HTTPStatus

import pytest

pytestmark = pytest.mark.asyncio


async def test_reg_bad(session, redis, event_loop, make_request, restart_db):
    res = await make_request('/api/v1/registration', json={'email': 'test', 'username': '123', 'password': 'pass'})
    assert res.status == HTTPStatus.BAD_REQUEST


async def test_reg(session, redis, event_loop, make_request, restart_db):
    res = await make_request('/api/v1/registration', json={'email': 'test@test.com',
                                                            'username': '123', 'password': 'pass'})
    assert res.status == HTTPStatus.OK


async def test_login(session, redis, event_loop, make_request, restart_db):
    await make_request('/api/v1/registration', json={'email': 'test@test.com',
                                                     'username': '123', 'password': 'pass'})
    res = await make_request('/api/v1/login', json={'username': '123', 'password': 'pass'})
    assert res.status == HTTPStatus.OK


async def test_logout(session, redis, event_loop, make_request, restart_db):
    await make_request('/api/v1/registration', json={'email': 'test@test.com',
                                                     'username': '123', 'password': 'pass'})
    res_login = await make_request('/api/v1/login', json={'username': '123', 'password': 'pass'})

    token = res_login.body['access_token']

    res = await make_request('/api/v1/logout', headers={'Authorization': f'Bearer {token}'})
    assert res.status == HTTPStatus.OK


async def test_profile(session, redis, event_loop, make_request, restart_db):
    await make_request('/api/v1/registration', json={'email': 'test@test.com',
                                                     'username': '123', 'password': 'pass'})
    res_login = await make_request('/api/v1/login', json={'username': '123', 'password': 'pass'})

    token = res_login.body['access_token']

    res = await make_request('/api/v1/profile',  headers={'Authorization': f'Bearer {token}'}, method_type_choice='get')
    assert res.status == HTTPStatus.OK
    assert res.body['username'] == '123'


async def test_history(session, redis, event_loop, make_request, restart_db):
    await make_request('/api/v1/registration', json={'email': 'test@test.com',
                                                     'username': '123', 'password': 'pass'})
    res_login = await make_request('/api/v1/login', json={'username': '123', 'password': 'pass'})

    token = res_login.body['access_token']
    res = await make_request('/api/v1/history',  headers={'Authorization': f'Bearer {token}'}, method_type_choice='get')

    assert res.status == HTTPStatus.OK
    assert len(res.body['history']) == 1


async def test_refresh(session, redis, event_loop, make_request, restart_db):
    await make_request('/api/v1/registration', json={'email': 'test@test.com',
                                                     'username': '123', 'password': 'pass'})
    res_login = await make_request('/api/v1/login', json={'username': '123', 'password': 'pass'})

    token = res_login.body['refresh_token']
    res = await make_request('/api/v1/refresh', headers={'Authorization': f'Bearer {token}'}, method_type_choice='post')
    assert res.status == HTTPStatus.OK


async def test_change_pass(session, redis, event_loop, make_request, restart_db):
    await make_request('/api/v1/registration', json={'email': 'test@test.com',
                                                     'username': '123', 'password': 'pass'})
    res_login = await make_request('/api/v1/login', json={'username': '123', 'password': 'pass'})

    token = res_login.body['access_token']

    res = await make_request('/api/v1/change_password',
                             json={'password': 'pass2'},
                             headers={'Authorization': f'Bearer {token}'},
                             method_type_choice='patch')

    assert res.status == HTTPStatus.OK
