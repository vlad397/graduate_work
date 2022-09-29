from functools import lru_cache

from db.database import FakeBaseDBService
from models.data_models.genre import Genre
from services.base import BaseService

fake_base_bd_service = FakeBaseDBService()


@lru_cache()
def get_stat_genre_service() -> BaseService:
    return BaseService("genre", fake_base_bd_service, Genre)
