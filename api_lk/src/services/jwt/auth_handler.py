import time

import jwt
from core.config import config


def decodeJWT(token: str) -> dict | None:
    try:
        decoded_token = jwt.decode(token, config.SECRET_KEY, algorithms=[config.JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return None
