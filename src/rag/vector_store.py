import chromadb

from src.config.settings import settings
from src.rag.embeddings import EmbeddingModel


class VectorStore:
    """
    ChromaDB vector store for FAQ documents.
    """

    def __init__(
        self,
        collection_name: str = "customer_support_faq"
    ):

        self.embedding_model = EmbeddingModel()

        self.client = chromadb.PersistentClient(
            path=str(settings.VECTOR_DB_DIR)
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )

    def add_documents(
        self,
        chunks: list[dict]
    ):

        texts = [
            chunk["text"]
            for chunk in chunks
        ]

        metadatas = [
            chunk["metadata"]
            for chunk in chunks
        ]

        ids = [
            f"{metadata['faq_id']}_{metadata['chunk_id']}"
            for metadata in metadatas
        ]

        embeddings = self.embedding_model.encode_documents(
            texts
        )

        self.collection.upsert(
            ids=ids,
            documents=texts,
            metadatas=metadatas,
            embeddings=embeddings.tolist()
        )

        print(
            f"Added {len(texts)} chunks to ChromaDB."
        )

    def search(
        self,
        query: str,
        top_k: int = 5
    ):

        query_embedding = (
            self.embedding_model.encode_query(query)
        )

        results = self.collection.query(
            query_embeddings=[
                query_embedding.tolist()
            ],
            n_results=top_k
        )

        return results


if __name__ == "__main__":

    from src.rag.document_loader import load_faq_documents
    from src.rag.chunking import create_chunks

    documents = load_faq_documents()

    chunks = create_chunks(documents)

    vector_store = VectorStore()

    vector_store.add_documents(chunks)

    print("\nVector database count:")
    print(vector_store.collection.count())

    results = vector_store.search(
        "I want to return my product",
        top_k=3
    )

    print("\nSearch Results:")

    for document, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):

        print("\n" + "=" * 60)
        print("Metadata:", metadata)
        print("Distance:", distance)
        print("Document:", document)