import logging
from typing import Coroutine

import backoff
from core import config
from core.utils import coroutine
from db.pg import PostgresExtractor

logger = logging.getLogger(__name__)


@coroutine
@backoff.on_exception(backoff.expo, (Exception,))
def coroutine_enricher(target: Coroutine, pg_table_m2m: str, pg_in_column: str):

    sql = f"""
        SELECT DISTINCT film_work_id AS id
        FROM {pg_table_m2m}
        WHERE {pg_in_column} IN %s
    """

    while rows := (yield):
        logger.info("Received: %s", len(rows))

        ids = tuple(row["id"] for row in rows)

        for fetched_rows in PostgresExtractor(config=config, sql=sql, sql_args=(ids,)):
            logger.info("Sending: %s to target coroutine", len(fetched_rows))
            target.send(fetched_rows)
