import os

from pydantic import BaseSettings, Field


class Config(BaseSettings):
    project_name: str = Field(env='PROJECT_NAME', default='auth')
    redis_host: str = Field(env='REDIS_HOST', default='redis_auth')
    redis_port: int = Field(env='REDIS_PORT', default=6379)
    postrges_user: str = Field(env='POSTGRES_USER', default='user')
    postrges_pass: str = Field(env='POSTGRES_PASS', default='pass')
    postrges_db: str = Field(env='POSTGRES_DATABASE', default='db')
    postrges_host: str = Field(env='POSTGRES_HOST', default='localhost')
    jwt_algorithm: str = Field(env='JWT_ALGORITHM', default='HS256')
    jwt_access_expire: int = Field(env="JWT_ACCESS_EXPIRE", default=600)
    jwt_expire: int = Field(env="JWT_EXPIRE", default=6000)
    salt: str = Field(env='SALT', default='salt')
    salt_user: str = Field(env='SALT_USER', default='salt_user')
    secret_key: str = Field(env='SECRET_KEY', default='secret_key')
    limit_requests: int = Field(env="LIMIT_REQUESTS", default=100)
    google_client_id: str = Field(env='GOOGLE_CLIENT_ID', default='google_client_id')
    google_secret_id: str = Field(env='GOOGLE_SECRET_ID', default='google_secret_id')
    google_server_metadata_url: str = Field(env='GOOGLE_METADATA_URL',
                                            default='https://accounts.google.com/.well-known/openid-configuration')
    twitter_client_id: str = Field(env='TWITTER_CLIENT_ID', default='twitter_client_id')
    twitter_secret_id: str = Field(env='TWITTER_SECRET_ID', default='twitter_secret_id')
    twitter_api_base_url: str = Field(env='TWITTER_API_BASE_URL', default='https://api.twitter.com/1.1/')
    twitter_request_token_url: str = Field(env='TWITTER_REQUEST_TOKEN_URL',
                                           default='https://api.twitter.com/oauth/request_token')
    twitter_access_token_url: str = Field(env='TWITTER_ACCESS_TOKEN_URL',
                                          default='https://api.twitter.com/oauth/access_token')
    twitter_authorize_url: str = Field(env='TWITTER_AUTHORIZE_TOKEN_URL',
                                       default='https://api.twitter.com/oauth/authenticate')
    server_url: str = Field(env='SERVER_URL')
    notification_service_endpoint: str = Field(env='NOTIFICATION_SERVICE_ENDPOINT')
    email_verify_body_name: str = Field(env='EMAIL_VERIFY_BODY_NAME')
    email_verify_header_name: str = Field(env='EMAIL_VERIFY_HEADER_NAME')
    verify_channel: str = Field(env='VERIFY_CHANNEL')


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

config = Config()
