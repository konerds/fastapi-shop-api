import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    ENV: str = os.getenv("ENV", "dev")
    DB_URL: str = os.getenv("DB_URL", "sqlite:///")


settings = Settings()
