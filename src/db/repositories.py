from sqlalchemy import select, delete
from sqlalchemy.orm import Session, joinedload

from db.models import Order, Member, Product, OrderedProduct
from dependencies import convert_order_status, convert_delivery_status


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

    def get_one(self, product_id: int):
        return self.session.scalar(
            select(Product)
            .where(Product.id == product_id)
        )

    def get_one_by_name(self, name: str):
        return self.session.scalar(
            select(Product)
            .where(Product.name == name)
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
        orders_raw = self.session.execute(
            select(Order)
            .options(
                joinedload(Order.member),
                joinedload(Order.delivery),
                joinedload(Order.ordered_products)
                .joinedload(OrderedProduct.product)
            )
            .order_by(
                Order.created_at.desc()
                if is_desc else
                Order.created_at
            )
        ).unique().scalars()
        orders = []
        for order in orders_raw:
            order_data = {
                "created_at": order.created_at,
                "updated_at": order.updated_at,
                "order_id": order.id,
                "member_id": order.member_id,
                "member_name": order.member.name,
                "address": order.delivery.address,
                "order_status": convert_order_status(order.get_status()),
                "delivery_created_at": order.delivery.created_at,
                "delivery_updated_at": order.delivery.updated_at,
                "delivery_status": convert_delivery_status(order.delivery.get_status()),
                "products": []
            }
            for ordered_product in order.ordered_products:
                product = ordered_product.product
                product_data = {
                    "quantity": ordered_product.quantity,
                    "name": product.name,
                    "price": ordered_product.price
                }
                order_data["products"].append(product_data)
            orders.append(order_data)
        return orders

    def get_all_by_member_id(self, member_id: int, is_desc: bool = True):
        orders_raw = self.session.execute(
            select(Order)
            .where(Order.member_id == member_id)
            .options(
                joinedload(Order.delivery),
                joinedload(Order.ordered_products)
                .joinedload(OrderedProduct.product)
            )
            .order_by(
                Order.created_at.desc()
                if is_desc else
                Order.created_at
            )
        ).unique().scalars()
        orders = []
        for order in orders_raw:
            order_data = {
                "created_at": order.created_at,
                "updated_at": order.updated_at,
                "order_id": order.id,
                "address": order.delivery.address,
                "order_status": convert_order_status(order.get_status()),
                "delivery_created_at": order.delivery.created_at,
                "delivery_updated_at": order.delivery.updated_at,
                "delivery_status": convert_delivery_status(order.delivery.get_status()),
                "products": []
            }
            for ordered_product in order.ordered_products:
                product = ordered_product.product
                product_data = {
                    "quantity": ordered_product.quantity,
                    "name": product.name,
                    "price": ordered_product.price
                }
                order_data["products"].append(product_data)
            orders.append(order_data)
        return orders

    def get_one(self, order_id: int):
        return self.session.scalar(
            select(Order)
            .where(Order.id == order_id)
            .options(
                joinedload(Order.delivery)
            )
        )

    def delete_one(self, order_id: int):
        self.session.execute(
            delete(Order)
            .where(Order.id == order_id)
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

    def get_one(self, member_id: int):
        return self.session.scalar(
            select(Member)
            .where(Member.id == member_id)
        )

    def get_one_by_email(self, email: str):
        return self.session.scalar(
            select(Member)
            .where(Member.email == email)
        )
