import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    ENV: str = os.getenv("ENV", "dev")
    PORT: int = int(os.getenv("PORT", 5000))
    DB_URL: str = os.getenv("DB_URL", "sqlite:///")
    SESSION_SECRET_KEY: str = os.getenv("SESSION_SECRET_KEY", "abcdzxcv12349876")
    ADMIN_EMAIL: str = os.getenv("ADMIN_EMAIL", "admin@konerds.buzz")
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "aaaaa11111")
    ADMIN_NAME: str = os.getenv("ADMIN_NAME", "admin")


settings = Settings()
