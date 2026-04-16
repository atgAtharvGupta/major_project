import os
from dataclasses import dataclass
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()

EMBEDDING_MODEL_ALIASES = {
    "bge-large": "BAAI/bge-large-en-v1.5",
    "bge-small-en": "BAAI/bge-small-en-v1.5",
    "bge-small": "BAAI/bge-small-en-v1.5",
    "BAAI/bge-large-en-v1.5": "BAAI/bge-large-en-v1.5",
    "BAAI/bge-small-en-v1.5": "BAAI/bge-small-en-v1.5",
}


def _clean_env(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()


def resolve_embedding_model(value: str) -> str:
    return EMBEDDING_MODEL_ALIASES.get(value.strip(), value.strip() or "BAAI/bge-large-en-v1.5")


@dataclass(frozen=True)
class Settings:
    neo4j_uri: str
    neo4j_username: str
    neo4j_password: str
    groq_api_key: str
    groq_model: str
    hf_token: str
    embedding_model: str
    google_api_key: str
    google_cse_id: str
    firebase_api_key: str
    firebase_auth_domain: str
    firebase_project_id: str
    firebase_storage_bucket: str
    firebase_messaging_sender_id: str
    firebase_app_id: str
    firebase_measurement_id: str
    firebase_web_config_json: str

    def missing_required(self, *names: str) -> list[str]:
        values = {
            "NEO4J_URI": self.neo4j_uri,
            "NEO4J_USERNAME": self.neo4j_username,
            "NEO4J_PASSWORD": self.neo4j_password,
            "GROQ_API_KEY": self.groq_api_key,
            "GOOGLE_API_KEY": self.google_api_key,
            "GOOGLE_CSE_ID": self.google_cse_id,
        }
        return [name for name in names if not values.get(name, "").strip()]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings(
        neo4j_uri=_clean_env("NEO4J_URI"),
        neo4j_username=_clean_env("NEO4J_USERNAME"),
        neo4j_password=_clean_env("NEO4J_PASSWORD"),
        groq_api_key=_clean_env("GROQ_API_KEY"),
        groq_model=_clean_env("GROQ_MODEL", "llama-3.3-70b-versatile"),
        hf_token=_clean_env("HF_TOKEN"),
        embedding_model=resolve_embedding_model(_clean_env("EMBEDDING_MODEL", "bge-large")),
        google_api_key=_clean_env("GOOGLE_API_KEY"),
        google_cse_id=_clean_env("GOOGLE_CSE_ID"),
        firebase_api_key=_clean_env("FIREBASE_API_KEY"),
        firebase_auth_domain=_clean_env("FIREBASE_AUTH_DOMAIN"),
        firebase_project_id=_clean_env("FIREBASE_PROJECT_ID"),
        firebase_storage_bucket=_clean_env("FIREBASE_STORAGE_BUCKET"),
        firebase_messaging_sender_id=_clean_env("FIREBASE_MESSAGING_SENDER_ID"),
        firebase_app_id=_clean_env("FIREBASE_APP_ID"),
        firebase_measurement_id=_clean_env("FIREBASE_MEASUREMENT_ID"),
        firebase_web_config_json=_clean_env("FIREBASE_WEB_CONFIG_JSON"),
    )


SETTINGS = get_settings()

NEO4J_URI = SETTINGS.neo4j_uri
NEO4J_USERNAME = SETTINGS.neo4j_username
NEO4J_PASSWORD = SETTINGS.neo4j_password
GROQ_API_KEY = SETTINGS.groq_api_key
GROQ_MODEL = SETTINGS.groq_model
HF_TOKEN = SETTINGS.hf_token
EMBEDDING_MODEL = SETTINGS.embedding_model
GOOGLE_API_KEY = SETTINGS.google_api_key
GOOGLE_CSE_ID = SETTINGS.google_cse_id
FIREBASE_API_KEY = SETTINGS.firebase_api_key
FIREBASE_AUTH_DOMAIN = SETTINGS.firebase_auth_domain
FIREBASE_PROJECT_ID = SETTINGS.firebase_project_id
FIREBASE_STORAGE_BUCKET = SETTINGS.firebase_storage_bucket
FIREBASE_MESSAGING_SENDER_ID = SETTINGS.firebase_messaging_sender_id
FIREBASE_APP_ID = SETTINGS.firebase_app_id
FIREBASE_MEASUREMENT_ID = SETTINGS.firebase_measurement_id
FIREBASE_WEB_CONFIG_JSON = SETTINGS.firebase_web_config_json
