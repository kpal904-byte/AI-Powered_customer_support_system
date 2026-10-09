from pathlib import Path
import pandas as pd

from src.config.settings import settings


def load_faq_data() -> pd.DataFrame:
    """
    Load FAQ data from CSV.
    """
    file_path = settings.RAW_DATA_DIR / "FAQs" / "faq.csv"

    if not file_path.exists():
        raise FileNotFoundError(
            f"FAQ file not found: {file_path}"
        )

    df = pd.read_csv(file_path)

    return df


def load_support_tickets() -> pd.DataFrame:
    """
    Load customer support ticket data.
    """
    file_path = (
        settings.RAW_DATA_DIR
        / "support_tickets"
        / "support_tickets.csv"
    )

    if not file_path.exists():
        raise FileNotFoundError(
            f"Support ticket file not found: {file_path}"
        )

    df = pd.read_csv(file_path)

    return df


def load_conversations() -> pd.DataFrame:
    """
    Load customer conversation data.
    """
    file_path = (
        settings.RAW_DATA_DIR
        / "customer_conversations"
        / "conversations.csv"
    )

    if not file_path.exists():
        raise FileNotFoundError(
            f"Conversation file not found: {file_path}"
        )

    df = pd.read_csv(file_path)

    return df


def load_all_data() -> dict:
    """
    Load all structured customer-support datasets.
    """

    return {
        "faq": load_faq_data(),
        "tickets": load_support_tickets(),
        "conversations": load_conversations(),
    }


if __name__ == "__main__":

    data = load_all_data()

    for name, df in data.items():

        print("\n" + "=" * 50)
        print(f"{name.upper()} DATA")
        print("=" * 50)

        print("Shape:", df.shape)
        print("Columns:", list(df.columns))
        print("\nFirst 5 rows:")
        print(df.head())