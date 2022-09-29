from typing import Type

from db.database import BaseDBService
from models.data_models.film import Film
from models.data_models.genre import Genre


class BaseService:
    model: Type[Film] | Type[Genre]
    db: BaseDBService
    type_service: str

    def __init__(self, type_service: str, db: BaseDBService, model: Type[Film] | Type[Genre]):
        self.model = model
        self.db = db
        self.type_service = type_service

    async def get_favourite(self, user_id: str | None, num: int) -> (list[Film] | list[Genre]) | None:
        if self.type_service == "genre":
            return await self.db.get_genres_by_user_id(user_id, self.model, num)
        elif self.type_service == "film":
            return await self.db.get_films_by_user_id(user_id, self.model, num)
        elif self.type_service == "best_film":
            return await self.db.get_best_films(self.model, num)
        raise NotImplemented(f"No service for this handle type {self.type_service}")
