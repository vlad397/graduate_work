from typing import Optional

from qdrant_client import QdrantClient

client: Optional[QdrantClient] = None


def get_qdrant_client() -> Optional[QdrantClient]:
    return client
