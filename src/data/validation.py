import pandas as pd


def validate_dataframe(
    df: pd.DataFrame,
    required_columns: list[str],
    dataset_name: str
) -> bool:
    """
    Validate basic quality of a dataframe.
    """

    print("\n" + "=" * 60)
    print(f"VALIDATING: {dataset_name}")
    print("=" * 60)

    # 1. Check required columns
    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        print(f"❌ Missing columns: {missing_columns}")
        return False

    print("✅ Required columns are present.")

    # 2. Check shape
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    # 3. Check missing values
    missing_values = df.isnull().sum()

    print("\nMissing values:")
    print(missing_values)

    if missing_values.sum() == 0:
        print("✅ No missing values found.")
    else:
        print("⚠️ Missing values found.")

    # 4. Check duplicate rows
    duplicates = df.duplicated().sum()

    print(f"\nDuplicate rows: {duplicates}")

    if duplicates == 0:
        print("✅ No duplicate rows found.")
    else:
        print("⚠️ Duplicate rows found.")

    return True


def validate_all_data(data: dict) -> None:
    """
    Validate all project datasets.
    """

    validate_dataframe(
        data["faq"],
        ["faq_id", "category", "question", "answer"],
        "FAQ DATA"
    )

    validate_dataframe(
        data["tickets"],
        [
            "ticket_id",
            "customer_id",
            "query",
            "intent",
            "priority",
            "status",
            "resolution"
        ],
        "SUPPORT TICKETS"
    )

    validate_dataframe(
        data["conversations"],
        [
            "conversation_id",
            "customer_id",
            "message",
            "intent",
            "speaker"
        ],
        "CUSTOMER CONVERSATIONS"
    )


if __name__ == "__main__":
    from src.data.data_loader import load_all_data

    data = load_all_data()
    validate_all_data(data)