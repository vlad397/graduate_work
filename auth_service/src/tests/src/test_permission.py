from http import HTTPStatus

import pytest

pytestmark = pytest.mark.asyncio


async def test_check(session, redis, event_loop, make_request, restart_db):
    res_login = await make_request('/api/v1/login', json={'username': 'superuser', 'password': 'pass'})
    token = res_login.body['access_token']
    res = await make_request('/api/v1/check_permission', json={'name': 'superuser'},
                             headers={'Authorization': f'Bearer {token}'}, method_type_choice='get')
    assert res.status == HTTPStatus.OK


async def test_grant(session, redis, event_loop, make_request, restart_db):
    res_login = await make_request('/api/v1/login', json={'username': 'superuser', 'password': 'pass'})
    token = res_login.body['access_token']
    res = await make_request('/api/v1/grant_permission', json={'username': 'superuser', 'role_name': 'premium'},
                             headers={'Authorization': f'Bearer {token}'}, method_type_choice='post')
    assert res.status == HTTPStatus.OK


async def test_take(session, redis, event_loop, make_request, restart_db):
    res_login = await make_request('/api/v1/login', json={'username': 'superuser', 'password': 'pass'})
    token = res_login.body['access_token']
    res = await make_request('/api/v1/take_permission', json={'username': 'superuser', 'role_name': 'superuser'},
                             headers={'Authorization': f'Bearer {token}'}, method_type_choice='delete')
    assert res.status == HTTPStatus.OK
