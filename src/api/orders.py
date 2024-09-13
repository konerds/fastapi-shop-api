from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from db.models import Order
from db.repositories import OrderRepository
from db.session import get_db
from schema.res import DtoResOrders, DtoResOrder

router = APIRouter(prefix="/api/orders")


@router.get("/")
def get_orders_handler(
        sort_type: str = Query(
            "asc",
            alias="sort_type"
        ),
        session: Session = Depends(get_db)
) -> DtoResOrders:
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
