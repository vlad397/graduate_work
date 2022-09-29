import logging
from typing import Coroutine

import backoff
from core import config
from core.utils import coroutine
from db.pg import PostgresExtractor

logger = logging.getLogger(__name__)

SQL = """
    SELECT
       fw.id                                    AS id,
       fw.title                                 AS film_title,
       fw.description                           AS film_description,      
       fw.rating                                AS imdb_rating
    FROM "content"."film_work" fw
           LEFT JOIN "content"."genre_film_work" fgw ON fw.id = fgw.film_work_id
           LEFT JOIN "content"."person_film_work" fwp ON fw.id = fwp.film_work_id
           LEFT JOIN "content"."genre" g ON fgw.genre_id = g.id
           LEFT JOIN "content"."person" p ON fwp.person_id = p.id
    WHERE fw.id IN %s
    GROUP BY fw.id
"""


@coroutine
@backoff.on_exception(backoff.expo, (Exception,))
def coroutine_merger(target: Coroutine):
    while rows := (yield):
        logger.info("Received: %s", len(rows))

        ids = tuple(row["id"] for row in rows)

        for fetched_rows in PostgresExtractor(config=config, sql=SQL, sql_args=(ids,)):
            logger.info("Sending: %s to target coroutine", len(fetched_rows))
            target.send(fetched_rows)
