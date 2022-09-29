import enum

from authlib.integrations.flask_client import OAuth
from core.config import config


class OAuthServices(enum.Enum):
    GOOGLE = 'google'
    TWITTER = 'twitter'

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


def registrate_services(oauth: OAuth):
    oauth.register(
        OAuthServices.GOOGLE.value,
        client_id=config.google_client_id,
        client_secret=config.google_secret_id,
        server_metadata_url=config.google_server_metadata_url,
        client_kwargs={'scope': 'openid profile email'},
    )
    oauth.register(
        name=OAuthServices.TWITTER.value,
        client_id=config.twitter_client_id,
        client_secret=config.twitter_secret_id,
        api_base_url=config.twitter_api_base_url,
        request_token_url=config.twitter_request_token_url,
        access_token_url=config.twitter_access_token_url,
        authorize_url=config.twitter_authorize_url,
    )
