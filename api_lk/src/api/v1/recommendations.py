import json
import uuid
from http import HTTPStatus

import requests
from core.config import config
from fastapi import APIRouter, Depends
from helpers import static_texts
from helpers.editors_choice import editors_films
from requests import (ConnectionError, ConnectTimeout, HTTPError, ReadTimeout,
                      Timeout)
from services.jwt.auth_bearer import JWTBearer

router = APIRouter()
jwt_bearer = JWTBearer()


@router.get("/recommendations", status_code=HTTPStatus.OK, response_description='Список рекомендуемых фильмов')
async def get_reccomendations(user_id: str = Depends(jwt_bearer)) -> list[uuid.UUID] | tuple[dict, HTTPStatus]:
    """
    Выдает список uuid рекомендуемых фильмов на основе топ 10 просмотренных фильмов с самым высоким рейтингом
    """
    if not user_id:
        return {"msg": static_texts.UNAUTH_401}, HTTPStatus.UNAUTHORIZED

    try:
        response_user_top_10 = requests.get(f"{config.stat_service.best_film_url}{user_id}")
        if response_user_top_10:
            user_top_10 = json.loads(response_user_top_10.text)
            fids = [film.get("id") for film in user_top_10]

            response_rec = requests.post(config.rec_service.rec_films_url, json={"ids": fids})
            if response_rec:
                rec_fids = json.loads(response_rec.text)
                return rec_fids

        response_global_top = requests.get(config.film_service.film_url)
        if response_global_top:
            films = json.loads(response_global_top.text)
            global_fids = [film.get("uuid") for film in films]
            return global_fids

        return editors_films

    except (ConnectTimeout, HTTPError, ReadTimeout, Timeout, ConnectionError):
        return editors_films
