import logging

import backoff
from core.utils import coroutine
from models.body import BatchQdrantPoints
from svc.qdrant import QdrantProcessor

logger = logging.getLogger(__name__)


@coroutine
@backoff.on_exception(backoff.expo, (Exception,))
def coroutine_loader(qd: QdrantProcessor):

    while data := (yield):
        qd_data = []
        for row in data:
            qd_data.append(row)
        batch = BatchQdrantPoints(qp_batch=qd_data)
        qd.insert_points(batch)
