from logging import config as logging_config

from core.logger import LOGGING
from pydantic import BaseSettings, Field

logging_config.dictConfig(LOGGING)


class Config(BaseSettings):
    DEBUG: bool = Field(True, env="DEBUG")
    PROJECT_NAME: str = Field("recommendation_api", env="PROJECT_NAME")
    QDRANT_HOST: str = Field("qdrant", env="QDRANT")
    QDRANT_PORT: int = Field(6333, env="QDRANT")
    QDRANT_COLLECTION: str = Field("films", env="QDRANT_COLLECTION")
    EMBEDDINGS_VECTOR_SIZE: int = Field(768, env="EMBEDDINGS_VECTOR_SIZE")


config = Config()
