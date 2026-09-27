from pathlib import Path
import re

from app.services.embedding.embedding_service import EmbeddingService
from app.services.milvus.milvus_service import MilvusService


DOCUMENTS_DIR = Path(__file__).parent / "documents"


def parse_document(
    file_path: Path,
) -> list[dict[str, str]]:
    content = file_path.read_text(
        encoding="utf-8"
    )

    sections = re.split(
        r"(?=^##\s+)",
        content,
        flags=re.MULTILINE,
    )

    documents: list[dict[str, str]] = []

    for section in sections:
        section = section.strip()

        if not section.startswith("## "):
            continue

        lines = section.splitlines()

        heading = lines[0].removeprefix("## ").strip()

        match = re.match(
            r"([A-Z]+-\d+)\s*-\s*(.+)",
            heading,
        )

        if not match:
            continue

        error_code = match.group(1)
        title = match.group(2).strip()

        section_content = "\n".join(
            lines[1:]
        ).strip()

        documents.append(
            {
                "error_code": error_code,
                "title": title,
                "content": section_content,
            }
        )

    return documents


def load_documents() -> list[dict[str, str]]:
    documents: list[dict[str, str]] = []

    for file_path in sorted(
        DOCUMENTS_DIR.glob("*.md")
    ):
        documents.extend(
            parse_document(file_path)
        )

    return documents


def seed() -> None:
    documents = load_documents()

    if not documents:
        raise RuntimeError(
            "No knowledge base documents found."
        )

    embedding_service = EmbeddingService()
    milvus_service = MilvusService()

    milvus_service.initialize_collection()

    texts = [
        (
            f"Error Code: {document['error_code']}\n"
            f"Title: {document['title']}\n"
            f"{document['content']}"
        )
        for document in documents
    ]

    vectors = embedding_service.embed_many(texts)

    records = []

    for index, document in enumerate(documents):
        records.append(
            {
                "id": index,
                "vector": vectors[index],
                "error_code": document["error_code"],
                "title": document["title"],
                "content": document["content"],
            }
        )

    milvus_service.insert(records)

    print(
        f"Inserted {len(records)} knowledge records."
    )


if __name__ == "__main__":
    seed()