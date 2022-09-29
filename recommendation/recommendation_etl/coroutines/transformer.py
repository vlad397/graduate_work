import logging
from typing import Coroutine

import backoff
from core.utils import coroutine

logger = logging.getLogger(__name__)


@coroutine
@backoff.on_exception(backoff.expo, (Exception,))
def coroutine_transformer(target: Coroutine):
    while rows := (yield):
        dicts = list(map(dict, rows))

        logger.info("Sending: %s to target coroutine", len(dicts))
        target.send(dicts)
