from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from db.models import Order
from db.session import get_db
from schemas.res import DtoResOrders, DtoResOrder

router = APIRouter()


@router.get("/orders/")
def get_orders_handler(
        session: Session = Depends(get_db),
        sort_type: str = Query(
            "asc",
            alias="sort-type"
        )
) -> DtoResOrders:
    orders: List[Order] = list(session.scalars(select(Order)))
    if sort_type == "desc":
        return DtoResOrders(
            orders=[DtoResOrder.model_validate(order) for order in orders[::-1]]
        )
    return DtoResOrders(
        orders=[DtoResOrder.model_validate(order) for order in orders]
    )
