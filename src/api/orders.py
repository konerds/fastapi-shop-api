from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from db.models import Order, OrderedProduct
from db.repositories import OrderRepository, MemberRepository, ProductRepository
from db.session import get_db
from schema.req import DtoReqPostOrder
from schema.res import DtoResOrders, DtoResOrder, DtoResOrderedProduct

router = APIRouter(prefix="/api/orders")


@router.get(
    "/",
    response_model=DtoResOrders
)
def get_orders_handler(
        sort_type: str = Query(
            "asc",
            alias="sort_type"
        ),
        session: Session = Depends(get_db)
):
    order_repository = OrderRepository(session)
    orders: List[Order] = order_repository.get_all(
        sort_type == "desc"
    )
    return DtoResOrders(
        data=[
            DtoResOrder.model_validate(order)
            for order in orders
        ]
    )


@router.post(
    "/",
    response_model=DtoResOrder
)
def post_order_handler(
        req: DtoReqPostOrder,
        session: Session = Depends(get_db),
):
    member_repository = MemberRepository(session)
    member = member_repository.get_one(req.member_id)
    product_repository = ProductRepository(session)
    product = product_repository.get_one(req.product_id)
    ordered_product = OrderedProduct.create(product, req.quantity)
    order_repository = OrderRepository(session)
    order = order_repository.save(
        Order.create(
            member=member,
            ordered_products=[ordered_product]
        )
    )
    return DtoResOrder(
        id=order.id,
        member_id=order.member_id,
        products=[DtoResOrderedProduct(
            id=product.id,
            name=product.name,
            price=product.price,
            quantity=req.quantity
        )]
    )
