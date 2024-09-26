from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker

from core.config import settings
from db.models import Base

if settings.ENV == "prod":
    engine = create_engine(
        settings.DB_URL,
        pool_pre_ping=True
    )
else:
    engine = create_engine(
        settings.DB_URL,
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

Base.metadata.create_all(bind=engine)
