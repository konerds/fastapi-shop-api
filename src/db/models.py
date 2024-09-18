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


class Product(Base, MixinDefault):
    __tablename__ = "products"

    name = Column(
        String(256),
        nullable=False,
        unique=True
    )
    price = Column(
        Integer,
        nullable=False
    )
    stock = Column(
        Integer,
        nullable=False
    )

    def increase_stock(self, amount: int):
        self.stock += amount

    def decrease_stock(self, amount: int):
        self.stock = max(0, self.stock - amount)

    def get_price(self):
        return self.price

    @classmethod
    def create(cls, name: str, price: int, stock: int = 0):
        return cls(
            name=name,
            price=price,
            stock=stock
        )


class OrderedProduct(Base, MixinDefault):
    __tablename__ = "ordered_products"

    quantity = Column(
        Integer,
        nullable=False
    )

    product_id = Column(
        Integer,
        ForeignKey("products.id")
    )
    order_id = Column(
        Integer,
        ForeignKey("orders.id")
    )

    product = relationship(
        "Product"
    )
    order = relationship(
        "Order",
        back_populates="ordered_products"
    )

    @classmethod
    def create(cls, product: Product, quantity: int):
        return cls(
            product_id=product.id,
            product=product,
            quantity=quantity
        )


class Member(Base, MixinDefault):
    __tablename__ = "members"

    email = Column(
        String(256),
        nullable=False,
        unique=True,
        index=True
    )

    password = Column(
        String(256),
        nullable=False
    )

    name = Column(
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
    def create(cls, email: str, password: str, name: str):
        return cls(
            email=email,
            password=password,
            name=name
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

    ordered_products = relationship(
        "OrderedProduct",
        back_populates="order"
    )

    delivery_id = Column(
        Integer,
        ForeignKey("deliveries.id")
    )

    delivery = relationship(
        "Delivery",
        back_populates="order",
        uselist=False
    )

    def __repr__(self):
        return f"Order(id={self.id})"

    def add_ordered_product(self, ordered_product: OrderedProduct):
        ordered_product.order = self
        ordered_product.order_id = self.id
        self.ordered_products.append(ordered_product)

    @classmethod
    def create(cls, member: Member, ordered_products: list[OrderedProduct]):
        order = cls(
            member_id=member.id,
            member=member,
            ordered_products=ordered_products
        )
        for ordered_product in ordered_products:
            order.add_ordered_product(ordered_product)
        return order


class Delivery(Base, MixinDefault):
    __tablename__ = "deliveries"

    address = Column(
        String(256),
        nullable=False
    )

    order = relationship(
        "Order",
        back_populates="delivery",
        uselist=False
    )
