from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_USER: str = "loja_user"
    DB_PASSWORD: str = "loja_password"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "loja_db"
    DATABASE_URL: str | None = None
    ENVIRONMENT: str = "production"

    @property
    def database_url(self) -> str:
        # Se a DATABASE_URL for definida (permite usar Postgres em produção)
        if self.DATABASE_URL:
            return self.DATABASE_URL
        # Em desenvolvimento, usar SQLite
        if self.ENVIRONMENT == "development":
            return "sqlite:///./test.db"

        user, pwd, host, port, db = (
            self.DB_USER,
            self.DB_PASSWORD,
            self.DB_HOST,
            self.DB_PORT,
            self.DB_NAME,
        )
        return f"postgresql+psycopg://{user}:{pwd}@{host}:{port}/{db}"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="allow"
    )


settings = Settings()
