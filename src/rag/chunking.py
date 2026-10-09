from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.config.settings import settings
from src.rag.document_loader import load_faq_documents


def create_chunks(documents: list[dict]) -> list[dict]:
    """
    Split documents into smaller chunks.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ],
    )

    chunks = []

    for document in documents:

        split_texts = splitter.split_text(
            document["text"]
        )

        for index, chunk_text in enumerate(split_texts):

            metadata = document["metadata"].copy()

            metadata["chunk_id"] = index

            chunks.append({
                "text": chunk_text,
                "metadata": metadata,
            })

    return chunks


if __name__ == "__main__":

    documents = load_faq_documents()

    chunks = create_chunks(documents)

    print("Documents:", len(documents))
    print("Chunks:", len(chunks))

    for chunk in chunks[:3]:

        print("\n" + "=" * 60)
        print(chunk["metadata"])
        print(chunk["text"])