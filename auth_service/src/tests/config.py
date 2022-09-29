from pydantic import BaseSettings, Field


class TestConfig(BaseSettings):
    redis_host: str = Field(env='REDIS_HOST', default='redis_auth')
    redis_port: str = Field(env='REDIS_PORT', default=6379)
    postrges_host: str = Field(env='POSTGRES_HOST', default='postgres_auth')
    postrges_port: str = Field(env='POSTGRES_PORT', default=5432)
    postrges_db: str = Field(env='POSTGRES_DB', default='db')
    postrges_user: str = Field(env='POSTGRES_USER', default='user')
    postrges_pass: str = Field(env='POSTGRES_PASS', default='pass')
    service_url: str = Field(env='SERVICE_URL', default='http://auth_service:8000/')
