from logging import config as logging_config
from typing import List

from core.logger import LOGGING
from pydantic import BaseSettings, Field, PostgresDsn, RedisDsn

logging_config.dictConfig(LOGGING)


class Config(BaseSettings):
    DEBUG: bool = Field(True, env="DEBUG")
    PROJECT_NAME: str = Field("recommendation_etl", env="PROJECT_NAME")
    REDIS: RedisDsn = Field("redis://redis:6359/10", env="REDIS")
    EMBEDDINGS_GENERATOR_URL: str = Field(
        " http://recommendation_api:8080/api/v1/recommendation/generate-embeddings/", env="EMBEDDINGS_GENERATOR_URL"
    )
    POSTGRES: PostgresDsn = Field("postgresql://postgres:postgres@posgres:5432/postgres", env="POSTGRES")
    QDRANT_HOST: str = Field("qdrant", env="QDRANT")
    QDRANT_PORT: int = Field(6333, env="QDRANT")
    QDRANT_COLLECTION: str = Field("films", env="QDRANT_COLLECTION")
    EMBEDDINGS_VECTOR_SIZE: int = Field(768, env="EMBEDDINGS_VECTOR_SIZE")
    TARGET_TABLE_NAMES: List[str] = ["genre", "person"]
    BATCH_SIZE: int = 50
    REPEAT: int = 10


config = Config()
