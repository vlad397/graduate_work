from functools import lru_cache

from db.database import FakeBaseDBService
from models.data_models.film import Film
from services.base import BaseService

fake_base_bd_service = FakeBaseDBService()


@lru_cache()
def get_stat_film_service() -> BaseService:
    return BaseService("film", fake_base_bd_service, Film)


@lru_cache()
def get_stat_best_film_service() -> BaseService:
    return BaseService("best_film", fake_base_bd_service, Film)
