from typing import Optional

import backoff
import numpy as np
from models.body import BatchQdrantPoints
from sentence_transformers import SentenceTransformer


class Transformer:
    def __init__(self):
        self.model = SentenceTransformer("distilbert-base-nli-stsb-mean-tokens", device="cpu")

    @backoff.on_exception(backoff.expo, exception=(Exception,))
    def predict(self, data: list[str]) -> np.ndarray:
        return self.model.encode(data)

    @staticmethod
    def preprocessing(qd: BatchQdrantPoints):
        return [f"{p.film_title}.{p.film_description}" for p in qd.qp_batch]

    @staticmethod
    def postprocessing(embeddings: np.ndarray) -> list:
        return embeddings.tolist()

    def processing(self, qd: BatchQdrantPoints) -> list[list[float]]:
        prep_data = self.preprocessing(qd)
        embeddings = self.predict(prep_data)
        return self.postprocessing(embeddings)


transformer: Optional[Transformer] = None


def get_transformer() -> Optional[Transformer]:
    return transformer
