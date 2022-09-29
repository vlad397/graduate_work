from http import HTTPStatus

import pytest

pytestmark = pytest.mark.asyncio


async def test_change(session, redis, event_loop, make_request, restart_db):
    res_login = await make_request('/api/v1/login', json={'username': 'superuser', 'password': 'pass'})
    token = res_login.body['access_token']
    await make_request('/api/v1/create_role', json={'name': 'test'},
                       headers={'Authorization': f'Bearer {token}'}, method_type_choice='post')

    res = await make_request('/api/v1/change_role', json={'old_name': 'test', 'new_name': 'test1'},
                             headers={'Authorization': f'Bearer {token}'}, method_type_choice='patch')
    assert res.status == HTTPStatus.OK


async def test_create(session, redis, event_loop, make_request, restart_db):
    res_login = await make_request('/api/v1/login', json={'username': 'superuser', 'password': 'pass'})
    token = res_login.body['access_token']
    res = await make_request('/api/v1/create_role', json={'name': 'test'},
                             headers={'Authorization': f'Bearer {token}'}, method_type_choice='post')
    assert res.status == HTTPStatus.OK


async def test_delete(session, redis, event_loop, make_request, restart_db):
    res_login = await make_request('/api/v1/login', json={'username': 'superuser', 'password': 'pass'})
    token = res_login.body['access_token']
    await make_request('/api/v1/create_role', json={'name': 'test'},
                       headers={'Authorization': f'Bearer {token}'}, method_type_choice='post')

    res = await make_request('/api/v1/delete_role', json={'name': 'test'},
                             headers={'Authorization': f'Bearer {token}'}, method_type_choice='delete')
    assert res.status == HTTPStatus.OK


async def test_list(session, redis, event_loop, make_request, restart_db):
    res_login = await make_request('/api/v1/login', json={'username': 'superuser', 'password': 'pass'})
    token = res_login.body['access_token']
    await make_request('/api/v1/create_role', json={'name': 'test'},
                       headers={'Authorization': f'Bearer {token}'}, method_type_choice='post')
    res = await make_request('/api/v1/list_role',
                             headers={'Authorization': f'Bearer {token}'}, method_type_choice='get')
    assert res.status == HTTPStatus.OK
    assert len(res.body['roles']) == 3
