from http import HTTPStatus

import pytest

pytestmark = pytest.mark.asyncio


async def test_film_requests(session, event_loop, make_get_request):
    res = await make_get_request("api/v1/stat/film_last_view/1")

    assert res.status == HTTPStatus.OK
    assert len(res.body) == 10


async def test_genre_requests(session, event_loop, make_get_request):
    res = await make_get_request("api/v1/stat/genre_last_view/1")

    assert res.status == HTTPStatus.OK
    assert len(res.body) == 3


async def test_best_film_requests(session, event_loop, make_get_request):
    res = await make_get_request("api/v1/stat/best_films")

    assert res.status == HTTPStatus.OK
    assert len(res.body) == 10
    assert res.body == 10
