from pydantic import BaseSettings, Field


class TestConfig(BaseSettings):
    service_url: str = Field(env="SERVICE_URL", default="http://stat_service:8000/")
