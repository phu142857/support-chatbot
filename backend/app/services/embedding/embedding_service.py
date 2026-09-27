from sentence_transformers import SentenceTransformer


class EmbeddingService:
    MODEL_NAME = "all-MiniLM-L6-v2"
    VECTOR_DIMENSION = 384

    def __init__(self) -> None:
        self._model = SentenceTransformer(self.MODEL_NAME)

    def embed(self, text: str) -> list[float]:
        if not text.strip():
            raise ValueError("Text cannot be empty.")

        vector = self._model.encode(
            text,
            normalize_embeddings=True,
        )

        return vector.tolist()

    def embed_many(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        if not texts:
            return []

        vectors = self._model.encode(
            texts,
            normalize_embeddings=True,
        )

        return vectors.tolist()