from app.services.embedding.embedding_service import EmbeddingService
from app.services.milvus.milvus_service import MilvusService


class RetrievalService:
    def __init__(
        self,
        embedding_service: EmbeddingService,
        milvus_service: MilvusService,
    ) -> None:
        self._embedding_service = embedding_service
        self._milvus_service = milvus_service

    def search(
        self,
        error_code: str | None,
        error_message: str | None,
        limit: int = 3,
    ) -> list[dict]:
        query_parts: list[str] = []

        if error_code:
            query_parts.append(
                f"Error Code: {error_code}"
            )

        if error_message:
            query_parts.append(error_message)

        if not query_parts:
            return []

        query = "\n".join(query_parts)

        vector = self._embedding_service.embed(query)

        results = self._milvus_service.search(
            vector=vector,
            limit=limit,
        )

        return results