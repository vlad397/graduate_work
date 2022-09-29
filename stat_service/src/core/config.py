import os
from logging import config as logging_config

from core.logger import LOGGING
from pydantic import BaseSettings, Field

logging_config.dictConfig(LOGGING)


class Config(BaseSettings):
    project_name: str = Field(env="PROJECT_NAME", default="stat_service")
    path_fake_films: str = Field(env="FILMS_DB", default="/usr/app/fake_film_db.txt")
    path_fake_genres: str = Field(env="GENRES_DB", default="/usr/app/fake_genre_db.txt")


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

config = Config()
