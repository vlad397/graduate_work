from core.config import config
from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .auth_handler import decodeJWT


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = False):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            user_id = self.verify_jwt(credentials.credentials)
            if not user_id:
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return user_id
        else:
            if config.TEST:
                return "test"
            return None

    def verify_jwt(self, jwtoken: str) -> bool | None:
        try:
            payload = decodeJWT(jwtoken)
            user_id = payload["JWT_IDENTITY_CLAIM"]
        except:
            user_id = None
        return user_id
