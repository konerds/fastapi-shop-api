import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker

from db.models import Base

load_dotenv()

DB_URL = os.getenv("DB_URL", "sqlite:///")

engine = create_engine(
    DB_URL,
    echo=True,
    connect_args={
        "check_same_thread": False
    },
    poolclass=StaticPool
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


Base.metadata.create_all(bind=engine)
