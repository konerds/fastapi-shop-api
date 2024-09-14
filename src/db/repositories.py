from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from db.models import Order, Member, Product


class ProductRepository:
    def __init__(self, session: Session):
        self.session = session

    def save(self, product: Product):
        self.session.add(instance=product)
        self.session.commit()
        self.session.refresh(instance=product)
        return product

    def get_all(self, is_desc: bool = True):
        return list(
            self.session.scalars(
                select(Product)
                .order_by(
                    Product.created_at.desc()
                    if is_desc else
                    Product.created_at
                )
            )
        )

    def get_one(self, product_id):
        return self.session.scalar(
            select(Product)
            .where(product_id == Product.id)
        )


class OrderRepository:
    def __init__(self, session: Session):
        self.session = session

    def save(self, order: Order):
        self.session.add(instance=order)
        self.session.commit()
        self.session.refresh(instance=order)
        return order

    def get_all(self, is_desc: bool = True):
        return list(
            self.session.scalars(
                select(Order)
                .order_by(
                    Order.created_at.desc()
                    if is_desc else
                    Order.created_at
                )
            )
        )

    def get_one(self, order_id):
        return self.session.scalar(
            select(Order)
            .where(order_id == Order.id)
        )

    def delete_one(self, order_id: int):
        self.session.execute(
            delete(Order)
            .where(order_id == Order.id)
        )


class MemberRepository:
    def __init__(self, session: Session):
        self.session = session

    def save(self, member: Member):
        self.session.add(instance=member)
        self.session.commit()
        self.session.refresh(instance=member)
        return member

    def get_all(self, is_desc: bool = True):
        return list(
            self.session.scalars(
                select(Member)
                .order_by(
                    Member.created_at.desc()
                    if is_desc else
                    Member.created_at
                )
            )
        )

    def get_one(self, member_id):
        return self.session.scalar(
            select(Member)
            .where(member_id == Member.id)
        )
