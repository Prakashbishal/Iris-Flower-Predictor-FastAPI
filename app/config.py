from dataclasses import dataclass
from pathlib import Path
import os

@dataclass(frozen=True)
class Settings:
    model_path: Path = Path(os.getenv("MODEL_PATH", "./model/saved_model_iris.pkl"))
    enable_wiki: bool = os.getenv("ENABLE_WIKI", "true").lower() in {"1", "true", "yes", "y"}
    wiki_timeout_sec: float = float(os.getenv("WIKI_TIMEOUT_SEC", "6"))
    wiki_user_agent: str = os.getenv("WIKI_USER_AGENT", "iris-fastapi/1.0")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()
