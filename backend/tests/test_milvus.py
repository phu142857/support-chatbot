from app.services.embedding.embedding_service import EmbeddingService
from app.services.milvus.milvus_service import MilvusService


def main() -> None:
    embedding_service = EmbeddingService()
    milvus_service = MilvusService()

    query = (
        "AUTH-001 "
        "Database connection failed"
    )

    vector = embedding_service.embed(query)

    results = milvus_service.search(
        vector,
        limit=3,
    )

    for result in results:
        print(
            {
                "id": result["id"],
                "distance": result["distance"],
                "entity": result["entity"],
            }
        )


if __name__ == "__main__":
    main()