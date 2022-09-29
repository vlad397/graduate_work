import json
from http import HTTPStatus

import requests
from core.config import config
from fastapi import APIRouter, Depends
from helpers import static_texts
from models.data_models.genre import Genre
from requests import ConnectionError, ConnectTimeout, HTTPError, ReadTimeout, Timeout
from services.jwt.auth_bearer import JWTBearer

router = APIRouter()
jwt_bearer = JWTBearer()


@router.get("/favourite_genres", status_code=HTTPStatus.OK, response_model=list[Genre],
            response_description='Топ 3 любимых жанра')
async def get_favourite_genres(user_id: str = Depends(jwt_bearer)) -> list[Genre] | tuple[dict, HTTPStatus]:
    """
    Выдает список объектов со следующей информацией:
    - **id**: UUID объекта в базе данных
    - **name**: Название жанра
    """
    if not user_id:
        return {"msg": static_texts.UNAUTH_401}, HTTPStatus.UNAUTHORIZED
    try:
        response = requests.get(f"{config.stat_service.favourite_genres_url}{user_id}")
        genres = json.loads(response.text)
        return genres
    except (ConnectTimeout, HTTPError, ReadTimeout, Timeout, ConnectionError):
        return {"msg": static_texts.NO_CONTENT_404}, HTTPStatus.NOT_FOUND
