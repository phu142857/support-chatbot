from pathlib import Path
from typing import Any

from pymilvus import MilvusClient


class MilvusService:
    COLLECTION_NAME = "support_knowledge"
    VECTOR_DIMENSION = 384

    def __init__(
        self,
        database_path: str = "data/milvus.db",
    ) -> None:
        path = Path(database_path)

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._client = MilvusClient(
            uri=str(path),
        )

    def initialize_collection(self) -> None:
        if self._client.has_collection(
            collection_name=self.COLLECTION_NAME
        ):
            return

        self._client.create_collection(
            collection_name=self.COLLECTION_NAME,
            dimension=self.VECTOR_DIMENSION,
            metric_type="COSINE",
            consistency_level="Strong",
        )

    def insert(
        self,
        records: list[dict[str, Any]],
    ) -> list[int]:
        if not records:
            return []

        self.initialize_collection()

        result = self._client.insert(
            collection_name=self.COLLECTION_NAME,
            data=records,
        )

        return result.get("ids", [])

    def search(
        self,
        vector: list[float],
        limit: int = 3,
    ) -> list[dict[str, Any]]:
        self.initialize_collection()

        self._client.load_collection(
            collection_name=self.COLLECTION_NAME,
        )

        results = self._client.search(
            collection_name=self.COLLECTION_NAME,
            data=[vector],
            limit=limit,
            output_fields=[
                "error_code",
                "title",
                "content",
            ],
        )

        if not results:
            return []

        return results[0]