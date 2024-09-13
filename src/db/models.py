from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import declarative_base, relationship

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
