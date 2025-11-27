from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os
from pathlib import Path
# Chemin vers le .env
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


# Variables
VERA_API_KEY = os.getenv("VERA_API_KEY")
VERA_ENDPOINT = os.getenv("VERA_ENDPOINT")

if not VERA_API_KEY or not VERA_ENDPOINT:
    raise RuntimeError("VERA_API_KEY or VERA_ENDPOINT is not defined in .env", VERA_API_KEY)

class Settings(BaseSettings):
    DATABASE_URL: str | None = None  # Railway la fournit
    POSTGRES_USER: str | None = None
    POSTGRES_PASSWORD: str | None = None
    POSTGRES_DB: str | None = None

    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60*24

    @property
    def database_url(self) -> str:
        """
        Retourne DATABASE_URL si définie (Railway),
        sinon génère l'URL locale (développement).
        """
        if self.DATABASE_URL:
            return self.DATABASE_URL

        # fallback local
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@localhost:5433/{self.POSTGRES_DB}"

    model_config = {
        "env_file": ".env",
        "extra": "ignore"
    }

settings = Settings()
