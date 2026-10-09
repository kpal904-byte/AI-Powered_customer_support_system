import pandas as pd

from src.config.settings import settings


def load_faq_documents() -> list[dict]:
    """
    Convert FAQ CSV rows into documents for the RAG pipeline.
    """

    file_path = settings.RAW_DATA_DIR / "FAQs" / "faq.csv"

    if not file_path.exists():
        raise FileNotFoundError(
            f"FAQ file not found: {file_path}"
        )

    df = pd.read_csv(file_path)

    documents = []

    for _, row in df.iterrows():

        text = (
            f"Question: {row['question']}\n"
            f"Answer: {row['answer']}"
        )

        metadata = {
            "faq_id": row["faq_id"],
            "category": row["category"],
            "source": "faq.csv",
        }

        documents.append({
            "text": text,
            "metadata": metadata,
        })

    return documents


if __name__ == "__main__":
    documents = load_faq_documents()

    print("Total documents:", len(documents))

    for document in documents[:3]:
        print("\n" + "=" * 60)
        print(document["metadata"])
        print(document["text"])