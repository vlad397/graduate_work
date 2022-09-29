from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query
from models.data_models.film import Film
from models.data_models.genre import Genre
from services.base import BaseService
from services.films import get_stat_best_film_service, get_stat_film_service
from services.genres import get_stat_genre_service

router = APIRouter()


@router.get("/film_last_view/{user_id}", response_model=list[Film],
            response_description='Последние 10 просмотренных фильмов')
async def film_last_view(
    user_id: str, num: int = Query(10), stat_service: BaseService = Depends(get_stat_film_service)
) -> list[Film]:
    """
    Выдает список объектов со следующей информацией:
    - **id**: UUID объекта в базе данных
    - **title**: Название кинопроизведения
    - **description**: Описание кинопроизведения
    - **imdb_rating**: Рейтинг кинопроизведения
    - **genre**: Список жанров кинопроизведения
    """

    list_of_films = await stat_service.get_favourite(user_id=user_id, num=num)
    if not list_of_films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return list_of_films


@router.get("/genre_last_view/{user_id}", response_model=list[Genre],
            response_description='Топ 3 любимых жанра')
async def genre_last_view(
    user_id: str, num: int = Query(3), stat_service: BaseService = Depends(get_stat_genre_service)
) -> list[Genre]:
    """
    Выдает список объектов со следующей информацией:
    - **id**: UUID объекта в базе данных
    - **name**: Название жанра
    """

    genre_list = await stat_service.get_favourite(user_id=user_id, num=num)
    if not genre_list:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return genre_list


@router.get("/best_films/{user_id}", response_model=list[Film],
            response_description='10 просмотренных фильмов с самой высокой оценкой')
async def best_film(
    num: int = Query(10), stat_service: BaseService = Depends(get_stat_best_film_service)
) -> list[Film]:
    """
    Выдает список объектов со следующей информацией:
    - **id**: UUID объекта в базе данных
    - **title**: Название кинопроизведения
    - **description**: Описание кинопроизведения
    - **imdb_rating**: Рейтинг кинопроизведения
    - **genre**: Список жанров кинопроизведения
    """

    best_film_list = await stat_service.get_favourite(user_id=None, num=num)
    if not best_film_list:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return best_film_list
