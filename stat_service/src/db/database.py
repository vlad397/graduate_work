import csv
import random
from abc import abstractmethod
from typing import Type

from core.config import config
from models.base import DefaultModel
from models.data_models.film import Film
from models.data_models.genre import Genre
from abc import ABC


class BaseDBService(ABC):
    @abstractmethod
    async def get_films_by_user_id(self, user_id: str, object_model: DefaultModel, num: int):
        pass

    @abstractmethod
    async def get_genres_by_user_id(self, user_id: str, object_model: DefaultModel, num: int):
        pass

    @abstractmethod
    async def get_best_films(self, object_model: DefaultModel, num: int):
        pass


class FakeBaseDBService(BaseDBService):
    films_list: list[Film]
    genres_list: list[Genre]

    def __init__(self):
        self.genres_list = []
        with open(config.path_fake_genres) as csvfile:
            reader = csv.DictReader(csvfile, delimiter="|")
            for row in reader:
                self.genres_list.append(Genre(id=row["id"], name=row["name"]))

        self.films_list = []
        with open(config.path_fake_films) as csvfile:
            reader = csv.DictReader(csvfile, delimiter="|")
            for row in reader:
                random.seed(a=row["id"])
                self.films_list.append(
                    Film(
                        id=row["id"],
                        title=row["title"],
                        description=row["description"],
                        imdb_rating=float(row["imdb_rating"]) if row["imdb_rating"] else None,
                        genre=random.sample(self.genres_list, 3),
                    )
                )

    async def get_films_by_user_id(self, user_id: str, object_model: Type[Film], num: int):
        random.seed(a=user_id)
        return random.sample(self.films_list, num)

    async def get_genres_by_user_id(self, user_id: str, object_model: Type[Genre], num: int):
        random.seed(a=user_id)
        return random.sample(self.genres_list, num)

    async def get_best_films(self, object_model: Type[Film], num: int):
        sorted_list = self.films_list.copy()
        sorted_list.sort(key=lambda x: x.imdb_rating, reverse=True)
        return sorted_list[:num]
