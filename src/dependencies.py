from passlib.context import CryptContext

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
        yield session
    finally:
        session.close()
