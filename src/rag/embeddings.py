from sentence_transformers import SentenceTransformer


class EmbeddingModel:
    """
    Wrapper around Sentence Transformer embedding model.
    """

    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    ):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)

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
        Generate embedding for a user query.
        """

        return self.model.encode(
            query,
            normalize_embeddings=True
        )


if __name__ == "__main__":

    embedding_model = EmbeddingModel()

    texts = [
        "How can I request a refund?",
        "My laptop is overheating."
    ]

    embeddings = embedding_model.encode_documents(texts)

    print("\nEmbedding shape:")
    print(embeddings.shape)

    query_embedding = embedding_model.encode_query(
        "I want my money back"
    )

    print("\nQuery embedding shape:")
    print(query_embedding.shape)