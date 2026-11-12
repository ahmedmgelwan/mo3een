import os
from pathlib import Path
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    APP_NAME: str = os.getenv("APP_NAME")
    APP_VERSION: str = os.getenv("APP_VERSION")
    OPEN_AI_KEY: str = os.getenv("OPEN_AI_API_KEY")
    GENERATION_MODEL_NAME: str = os.getenv("MODEL_NAME", "openai/gpt-oss-20b")
    EMBEDDING_MODEL_NAME: str = os.getenv(
        "EMBEDDING_MODEL_NAME", "BAAI/bge-small-en-v1.5"
    )
    BASE_URL: str = os.getenv("BASE_URL", "https://api.openai.com/v1")
    REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", 20))
    MAX_GENERATED_TOKENS: int = int(os.getenv("MAX_GENERATED_TOKENS"))
    PROJECT_ROOT: Path = Path(__file__).parent.parent
    DOCS_DIR: str = PROJECT_ROOT / os.getenv("DOCS_DIR")
    SUPPORTED_FILE_TYPES = ['.txt', '.md', '.pdf']  
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE_TOKENS", 200))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP_TOKENS", 50))
    COLLECTION_NAME: str = os.getenv("COLLECTION_NAME", "mo3een")
    CHROMA_DB_DIR: str =   PROJECT_ROOT / os.getenv("CHROMA_DB_DIR", "./chroma_db")
    TOP_K: int = int(os.getenv("TOP_K", 5))
    SCOPE: str = os.getenv("SCOPE", "default")

    if not APP_NAME or not APP_VERSION or not OPEN_AI_KEY:
        raise ValueError("Missing required environment variables")


config = Config()
