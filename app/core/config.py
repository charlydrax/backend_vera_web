from pydantic_settings import BaseSettings

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
