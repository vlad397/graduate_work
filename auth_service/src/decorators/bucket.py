import datetime
from functools import wraps
from http import HTTPStatus

from constants.response import MESSAGE
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request


class Bucket:

    def __init__(self, redis_conn, limit):
        self.redis_conn = redis_conn
        self.limit = limit

    def rate_limit(self, func):
        @wraps(func)
        def inner(*args, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            pipe = self.redis_conn.pipeline()
            now = datetime.datetime.now()
            key = f'{user_id}:{now.minute}'
            pipe.incr(key, 1)
            pipe.expire(key, 59)
            result = pipe.execute()

            request_number = result[0]

            if request_number > self.limit:
                return {MESSAGE: 'Too many requests'}, HTTPStatus.TOO_MANY_REQUESTS

            return func(*args, **kwargs)

        return inner
