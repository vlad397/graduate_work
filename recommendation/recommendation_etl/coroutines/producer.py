import logging
from datetime import datetime
from typing import Coroutine

import backoff
from core import config
from core.utils import coroutine
from db.pg import PostgresExtractor
from db.state_storage import State
from redis.client import Redis

logger = logging.getLogger(__name__)


@coroutine
@backoff.on_exception(backoff.expo, (Exception,))
def coroutine_producer(
    target: Coroutine,
    pg_table_with_schema: str,
    storage: Redis,
):

    logger.info("Creating state")
    state = State(redis_adapter=storage)

    sql = f"""
        SELECT id, modified_at
        FROM {pg_table_with_schema}
        WHERE modified_at > %s
        ORDER BY modified_at
    """

    while _ := (yield):
        datetime_last_update = state.get_state(pg_table_with_schema)
        datetime_last_update_iso = (
            datetime.fromisoformat(datetime_last_update) if datetime_last_update else datetime.min.isoformat()
        )
        logger.info("Last updated for %s is: %s", pg_table_with_schema, datetime_last_update_iso)

        for fetched_rows in PostgresExtractor(config=config, sql=sql, sql_args=(datetime_last_update_iso,)):
            logger.info("Sending: %s to target coroutine", len(fetched_rows))
            target.send(fetched_rows)

            logger.info("Saving state")
            updated_at_max_iso = fetched_rows[-1]["modified_at"].isoformat()
            state.set_state(key=pg_table_with_schema, value=updated_at_max_iso)
