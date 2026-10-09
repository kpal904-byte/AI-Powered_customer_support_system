from src.config.settings import settings
from src.rag.vector_store import VectorStore


class Retriever:
    """
    Retrieves the most relevant documents
    from the ChromaDB vector store.
    """

    def __init__(self, top_k: int | None = None):
        self.top_k = top_k or settings.TOP_K
        self.vector_store = VectorStore()

    def retrieve(self, query: str) -> list[dict]:
        """
        Retrieve relevant documents for a user query.
        """

        results = self.vector_store.search(
            query=query,
            top_k=self.top_k
        )

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        retrieved_documents = []

        for document, metadata, distance in zip(
            documents,
            metadatas,
            distances
        ):
            retrieved_documents.append(
                {
                    "text": document,
                    "metadata": metadata,
                    "distance": distance,
                }
            )

        return retrieved_documents


if __name__ == "__main__":

    retriever = Retriever(top_k=3)

    query = "I want my money back for my order"

    results = retriever.retrieve(query)

    print("\nQuery:")
    print(query)

    print("\nRetrieved Documents:")

    for index, result in enumerate(results, start=1):

        print("\n" + "=" * 60)
        print(f"Result {index}")

        print("Distance:")
        print(result["distance"])

        print("\nMetadata:")
        print(result["metadata"])

        print("\nText:")
        print(result["text"])