import re
import pandas as pd


def clean_text(text: str) -> str:
    """
    Clean and normalize text.
    """

    if pd.isna(text):
        return ""

    # Convert to string
    text = str(text)

    # Convert to lowercase
    text = text.lower()

    # Remove URLs
    text = re.sub(r"http\S+|www\S+", "", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    # Remove leading/trailing spaces
    text = text.strip()

    return text


def preprocess_faq(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess FAQ dataset.
    """

    df = df.copy()

    df["question_clean"] = df["question"].apply(clean_text)
    df["answer_clean"] = df["answer"].apply(clean_text)

    return df


def preprocess_tickets(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess support ticket dataset.
    """

    df = df.copy()

    df["query_clean"] = df["query"].apply(clean_text)
    df["resolution_clean"] = df["resolution"].apply(clean_text)

    return df


def preprocess_conversations(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess customer conversation dataset.
    """

    df = df.copy()

    df["message_clean"] = df["message"].apply(clean_text)

    return df


def preprocess_all_data(data: dict) -> dict:
    """
    Preprocess all datasets.
    """

    return {
        "faq": preprocess_faq(data["faq"]),
        "tickets": preprocess_tickets(data["tickets"]),
        "conversations": preprocess_conversations(data["conversations"])
    }


if __name__ == "__main__":
    from src.data.data_loader import load_all_data

    data = load_all_data()
    processed_data = preprocess_all_data(data)

    print("\nFAQ sample:")
    print(
        processed_data["faq"][
            ["question", "question_clean"]
        ].head()
    )

    print("\nTicket sample:")
    print(
        processed_data["tickets"][
            ["query", "query_clean"]
        ].head()
    )

    print("\nConversation sample:")
    print(
        processed_data["conversations"][
            ["message", "message_clean"]
        ].head()
    )