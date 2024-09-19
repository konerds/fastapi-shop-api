from passlib.context import CryptContext
from sqlalchemy import text

from core.config import settings
from db.session import SessionLocal

crypt_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def encrypt(data):
    return crypt_context.hash(data)


def verify(plain, encrypted):
    return crypt_context.verify(plain, encrypted)


def get_db():
    session = SessionLocal()
    try:
        if settings.ENV == "dev":
            session.execute(text("PRAGMA foreign_keys=ON;"))
        yield session
    finally:
        session.close()
