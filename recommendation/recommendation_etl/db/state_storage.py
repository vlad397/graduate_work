import abc
import json
import logging
from typing import Any, Optional

import backoff
from redis import Redis

logger = logging.getLogger(__name__)


class BaseStorage:
    @abc.abstractmethod
    def save_state(self, state: dict) -> None:
        pass

    @abc.abstractmethod
    def retrieve_state(self) -> dict:
        pass


class JsonFileStorage(BaseStorage):
    def __init__(self, file_path: Optional[str] = None):
        self.file_path = file_path

    def retrieve_state(self) -> dict:
        try:
            with open(self.file_path, mode="r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = []
        return data

    def save_state(self, state: dict) -> None:
        with open(self.file_path, mode="w", encoding="utf-8") as f:
            json.dump(state, f)


class RedisStorage(BaseStorage):
    def __init__(self, redis_adapter: Redis):
        self.redis_adapter = redis_adapter

    def retrieve_state(self) -> dict:
        data = {}
        for key in self.redis_adapter.keys():
            data[key] = self.redis_adapter.get(str(key))
        return data

    def save_state(self, state: dict) -> None:
        for key in state:
            self.redis_adapter.set(key, state[key])


class State:
    def __init__(self, redis_adapter: Redis):
        self.redis_adapter = redis_adapter

    @backoff.on_exception(backoff.expo, exception=Exception)
    def set_state(self, key: str, value: str) -> None:
        self.redis_adapter.set(key, value)

    @backoff.on_exception(backoff.expo, exception=Exception)
    def get_state(self, key: str) -> Any:
        if self.redis_adapter.exists(str(key)):
            return self.redis_adapter.get(str(key)).decode("utf-8")
        return None


def chunk_row(cursor, size=100):
    while True:
        rows = cursor.fetchmany(size)
        if not rows:
            break
        for row in rows:
            yield row


def list_to_sql_str(arr):
    s = "("
    for el in arr:
        s += f"'{str(el)}',"
    s = s[:-1]
    s += ")"
    return s
