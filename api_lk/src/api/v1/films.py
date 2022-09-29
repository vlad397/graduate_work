import json
from http import HTTPStatus

import requests
from core.config import config
from fastapi import APIRouter, Depends
from helpers import static_texts
from models.data_models.film import Film
from requests import ConnectionError, ConnectTimeout, HTTPError, ReadTimeout, Timeout
from services.jwt.auth_bearer import JWTBearer

router = APIRouter()
jwt_bearer = JWTBearer()


@router.get("/best_films", status_code=HTTPStatus.OK, response_model=list[Film],
            response_description='10 просмотренных фильмов с самой высокой оценкой')
async def get_user_best_films(user_id: str = Depends(jwt_bearer)) -> list[Film] | tuple[dict, HTTPStatus]:
    """
    Выдает список объектов со следующей информацией:
    - **id**: UUID объекта в базе данных
    - **title**: Название кинопроизведения
    - **description**: Описание кинопроизведения
    - **imdb_rating**: Рейтинг кинопроизведения
    - **genre**: Список жанров кинопроизведения
    """
    if not user_id:
        return {"msg": static_texts.UNAUTH_401}, HTTPStatus.UNAUTHORIZED
    try:
        response = requests.get(f"{config.stat_service.best_film_url}{user_id}")
        films = json.loads(response.text)
        return films
    except (ConnectTimeout, HTTPError, ReadTimeout, Timeout, ConnectionError):
        return {"msg": static_texts.NO_CONTENT_404}, HTTPStatus.NOT_FOUND


@router.get("/last_viewed", status_code=HTTPStatus.OK, response_model=list[Film],
            response_description='Последние 10 просмотренных фильмов')
async def get_last_viewed(user_id: str = Depends(jwt_bearer)) -> list[Film] | tuple[dict, HTTPStatus]:
    """
    Выдает список объектов со следующей информацией:
    - **id**: UUID объекта в базе данных
    - **title**: Название кинопроизведения
    - **description**: Описание кинопроизведения
    - **imdb_rating**: Рейтинг кинопроизведения
    - **genre**: Список жанров кинопроизведения
    """
    if not user_id:
        return {"msg": static_texts.UNAUTH_401}, HTTPStatus.UNAUTHORIZED
    try:
        response = requests.get(f"{config.stat_service.last_viewed_url}{user_id}")
        films = json.loads(response.text)
        return films
    except (ConnectTimeout, HTTPError, ReadTimeout, Timeout, ConnectionError):
        return {"msg": static_texts.NO_CONTENT_404}, HTTPStatus.NOT_FOUND
