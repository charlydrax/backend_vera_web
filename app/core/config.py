from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):

    # Variables pour la DB
    DATABASE_URL: str | None = None  # Railway la fournit
    POSTGRES_USER: str | None = None
    POSTGRES_PASSWORD: str | None = None
    POSTGRES_DB: str | None = None
    TELEGRAM_TOKEN: str | None = None
    VERA_ENDPOINT: str | None = None
    VERA_API_KEY: str | None = None
    SECRET_KEY: str | None = None
    VERA_USER_ID: str | None = None

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60*24

    @property
    def database_url(self) -> str:
        """
        Retourne DATABASE_URL si définie (Railway),
        sinon génère l'URL locale (développement).
        """
        if self.DATABASE_URL:
            return self.DATABASE_URL

        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@localhost:5433/{self.POSTGRES_DB}"

    class Config:
        env_file = str(Path(__file__).resolve().parent.parent.parent / ".env")
        env_file_encoding = "utf-8"
        extra = "ignore"

# Crée l'instance globale
settings = Settings()

# Vérification rapide des variables critiques
if not settings.VERA_API_KEY or not settings.VERA_ENDPOINT:
    raise RuntimeError("VERA_API_KEY or VERA_ENDPOINT is not defined")
