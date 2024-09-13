from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, FetchedValue
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class MixinDefault(object):
    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=FetchedValue(),
        onupdate=func.now()
    )


class Order(Base, MixinDefault):
    __tablename__ = "orders"

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


class Member(Base, MixinDefault):
    __tablename__ = "members"

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

    @classmethod
    def create(cls, name: str, address: str):
        return cls(
            name=name,
            address=address
        )
