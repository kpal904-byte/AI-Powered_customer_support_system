from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]


# ============================================================
# APPLICATION SETTINGS
# ============================================================

class Settings(BaseSettings):

    # -------------------------
    # Application
    # -------------------------
    APP_NAME: str = "AI Customer Support System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # -------------------------
    # LLM Configuration
    # -------------------------
    OPENAI_API_KEY: str = ""
    GROQ_API_KEY: str = ""

    OPENAI_MODEL: str = "gpt-4o-mini"
    GROQ_MODEL: str = "llama-3.3-70b-versatile"

    # -------------------------
    # Embedding Configuration
    # -------------------------
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

    # -------------------------
    # RAG Configuration
    # -------------------------
    CHUNK_SIZE: int = 800
    CHUNK_OVERLAP: int = 100

    TOP_K: int = 5

    # -------------------------
    # Paths
    # -------------------------
    DATA_DIR: Path = PROJECT_ROOT / "data"

    RAW_DATA_DIR: Path = PROJECT_ROOT / "data" / "raw"

    PROCESSED_DATA_DIR: Path = (
        PROJECT_ROOT / "data" / "processed"
    )

    VECTOR_DB_DIR: Path = PROJECT_ROOT / "vector_db"

    MODEL_DIR: Path = PROJECT_ROOT / "models"

    # -------------------------
    # API
    # -------------------------
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    # -------------------------
    # MLflow
    # -------------------------
    MLFLOW_TRACKING_URI: str = "mlruns"

    # -------------------------
    # Pydantic Settings
    # -------------------------
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


# ============================================================
# SETTINGS INSTANCE
# ============================================================

settings = Settings()