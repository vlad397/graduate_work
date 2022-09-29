from logging import config as logging_config
from urllib.parse import urljoin

from core.logger import LOGGING
from pydantic import BaseSettings, Field, validator

logging_config.dictConfig(LOGGING)


class StatServiceConfig(BaseSettings):
    base_url: str = Field(env="STAT_BASE_URL", default="http://nginx_stat_service:81/")
    best_film_endpoint: str = Field(env="STAT_BEST_FILM_ENDPOINT", default="api/v1/stat/best_films/")
    last_viewed_endpoint: str = Field(env="STAT_LAST_VIEWED_ENDPOINT", default="api/v1/stat/film_last_view/")
    favourite_genres_endpoint: str = Field(env="STAT_FAV_GENRES_ENDPOINT", default="api/v1/stat/genre_last_view/")
    best_film_url: str = ""
    last_viewed_url: str = ""
    favourite_genres_url: str = ""

    @validator("best_film_url")
    def build_best_film_url(cls, v, values):
        return urljoin(values["base_url"], values["best_film_endpoint"])

    @validator("last_viewed_url")
    def build_last_viewed_url(cls, v, values):
        return urljoin(values["base_url"], values["last_viewed_endpoint"])

    @validator("favourite_genres_url")
    def build_favourite_genres_url(cls, v, values):
        return urljoin(values["base_url"], values["favourite_genres_endpoint"])


class FilmServiceConfig(BaseSettings):
    base_url: str = Field(env="FILM_BASE_URL", default="http://film_api:8003/")
    film_endpoint: str = Field(env="FILM_ENDPOINT", default="api/v1/films/")
    film_url: str = ""

    @validator("film_url")
    def build_best_film_url(cls, v, values):
        return urljoin(values["base_url"], values["film_endpoint"])


class RecommendationServiceConfig(BaseSettings):
    base_url: str = Field(env="REC_BASE_URL", default="http://recommendation_api:8080/")
    rec_films_endpoint: str = Field(env="REC_FILMS_ENDPOINT", default="api/v1/recommendation/film-personal-top/")
    rec_films_url: str = ""

    @validator("rec_films_url")
    def build_best_film_url(cls, v, values):
        return urljoin(values["base_url"], values["rec_films_endpoint"])


class Config(BaseSettings):
    PROJECT_NAME: str = "lk"
    DEBUG: bool = Field(True, env="DEBUG")
    API_VERSION: str = "v1"
    JWT_ALGORITHM: str = Field(env="JWT_ALGORITHM", default="HS256")
    SECRET_KEY: str = Field(env="SECRET_KEY", default="secret_key")
    TEST: bool = Field(True, env="TEST")
    stat_service: StatServiceConfig = StatServiceConfig()
    film_service: FilmServiceConfig = FilmServiceConfig()
    rec_service: RecommendationServiceConfig = RecommendationServiceConfig()


config = Config()
