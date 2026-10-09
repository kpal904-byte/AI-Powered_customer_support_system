from sentence_transformers import SentenceTransformer

from src.config.settings import settings


class EmbeddingModel:
    """
    Wrapper around the Sentence Transformer embedding model.
    """

    def __init__(
        self,
        model_name: str | None = None
    ):
        self.model_name = (
            model_name or settings.EMBEDDING_MODEL
        )

        self.model = SentenceTransformer(
            self.model_name
        )

    def encode_documents(
        self,
        texts: list[str]
    ):
        """
        Generate embeddings for documents.
        """

        return self.model.encode(
            texts,
            show_progress_bar=True,
            normalize_embeddings=True
        )

    def encode_query(
        self,
        query: str
    ):
        """
        Generate embedding for a query.
        """

        return self.model.encode(
            query,
            normalize_embeddings=True
        )


if __name__ == "__main__":

    embedding_model = EmbeddingModel()

    embeddings = embedding_model.encode_documents(
        [
            "How can I request a refund?",
            "My laptop is overheating."
        ]
    )

    print("Embedding shape:")
    print(embeddings.shape)