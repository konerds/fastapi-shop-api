import os
from typing import List

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.params import Depends, Query
from pydantic import BaseModel
from sqlalchemy import Column, Integer, ForeignKey, String, create_engine, StaticPool, select
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Session

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
    bind=engine,
)


def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


Base = declarative_base()


class Order(Base):
    __tablename__ = "orders"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    member_id = Column(
        Integer,
        ForeignKey("members.id")
    )

    member = relationship(
        "Member",
        back_populates="orders"
    )

    def __repr__(self):
        return f"Order(id={self.id})"


class Member(Base):
    __tablename__ = "members"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    name = Column(
        String(256),
        nullable=False
    )
    address = Column(
        String(256),
        nullable=False
    )

    orders = relationship(
        "Order",
        back_populates="member"
    )

    def __repr__(self):
        return f"Member(id={self.id})"


Base.metadata.create_all(bind=engine)
app = FastAPI()


class DtoResHealth(BaseModel):
    status: str = "OK"


@app.get("/")
def check_health() -> DtoResHealth:
    return DtoResHealth(status="OK")


class DtoResOrder(BaseModel):
    id: int

    class Config:
        from_attributes = True

class DtoResOrders(BaseModel):
    orders: List[DtoResOrder]

@app.get("/orders/")
def get_orders_handler(
        session: Session = Depends(get_db),
        sort_type: str = Query("asc", alias="sort-type"),
) -> DtoResOrders:
    orders: List[Order] = list(session.scalars(select(Order)))
    if sort_type == "desc":
        return DtoResOrders(
            orders=[DtoResOrders.model_validate(order) for order in orders[::-1]]
        )
    return DtoResOrders(
        orders=[DtoResOrders.model_validate(order) for order in orders]
    )


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)