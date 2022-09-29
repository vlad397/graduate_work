import logging
from typing import Any

import backoff
import psycopg2.extras
from core.config import Config

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


class PostgresExtractor:
    @backoff.on_exception(backoff.expo, (Exception,))
    def __init__(self, config: Config, sql: str, sql_args: tuple[Any]):
        logger.info("Connecting to Postgres")
        DSL = {
            "dbname": config.POSTGRES.path.replace("/", ""),
            "user": config.POSTGRES.user,
            "password": config.POSTGRES.password,
            "host": config.POSTGRES.host,
            "port": config.POSTGRES.port,
        }
        self.connection = psycopg2.connect(**DSL)
        self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        logger.info("Connected to Postgres!")

        self.cursor.arraysize = config.BATCH_SIZE
        self.cursor.execute(sql, sql_args)

    def __iter__(self):
        return self

    def __next__(self) -> list[dict]:
        results = self.cursor.fetchmany()
        if not results:
            raise StopIteration
        return results

    def __del__(self):
        self.cursor.close()
        self.connection.close()
