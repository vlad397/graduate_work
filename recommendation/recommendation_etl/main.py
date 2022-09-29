import logging
import time

import redis
from core.config import config
from coroutines import coroutine_enricher, coroutine_loader, coroutine_merger, coroutine_producer, coroutine_transformer
from qdrant_client import QdrantClient
from svc.qdrant import QdrantProcessor

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


def etl(storage, qd):
    loader = coroutine_loader(qd)

    transformer = coroutine_transformer(loader)

    merger = coroutine_merger(transformer)

    extractor_filmwork = coroutine_producer(
        merger,
        storage=storage,
        pg_table_with_schema='"content"."film_work"',
    )

    enricher_person = coroutine_enricher(
        merger,
        pg_table_m2m='"content"."person_film_work"',
        pg_in_column="person_id",
    )

    extractor_person = coroutine_producer(
        enricher_person,
        storage=storage,
        pg_table_with_schema='"content"."person"',
    )

    enricher_genre = coroutine_enricher(
        merger,
        pg_table_m2m='"content"."genre_film_work"',
        pg_in_column="genre_id",
    )

    extractor_genre = coroutine_producer(
        enricher_genre,
        storage=storage,
        pg_table_with_schema='"content"."genre"',
    )

    coroutines_producers = (
        extractor_person,
        extractor_genre,
        extractor_filmwork,
    )

    while True:
        logger.info("Starting ETL again!")

        for coroutine in coroutines_producers:
            coroutine.send(1)

        time.sleep(config.REPEAT)


if __name__ == "__main__":

    logger = logging.getLogger(__name__)
    redis = redis.Redis(host=config.REDIS.host, port=config.REDIS.port, db=config.REDIS.path.replace("/", ""))
    client = QdrantClient(host=config.QDRANT_HOST, port=config.QDRANT_PORT)
    qp = QdrantProcessor(client)
    etl(redis, qp)
